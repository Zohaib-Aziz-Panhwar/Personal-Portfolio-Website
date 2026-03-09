"""
API routes for certificate management.
"""

import asyncio
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from bson import ObjectId
from bson.errors import InvalidId

from models import CertificateCreate, CertificateUpdate
from database import get_certificates_collection
from auth import verify_admin_password

# Create router instance
router = APIRouter()

# Thread pool executor for running pymongo operations
executor = ThreadPoolExecutor(max_workers=5)


def convert_objectid_to_str(doc):
    """Convert MongoDB ObjectId to string and format dates."""
    if not doc:
        return doc
    result = doc.copy()
    if "_id" in result:
        result["id"] = str(result["_id"])
        del result["_id"]
    if "created_at" in result:
        if isinstance(result["created_at"], datetime):
            if result["created_at"].tzinfo is None:
                result["created_at"] = result["created_at"].replace(tzinfo=timezone.utc).isoformat()
            else:
                result["created_at"] = result["created_at"].isoformat()
    return result


@router.get("/certificates")
async def get_certificates():
    """
    Get all certificates.
    Returns list of all certificates sorted by completion date (newest first).
    """
    try:
        collection = get_certificates_collection()
        if collection is None:
            print("[ERROR] Certificates collection is None - database not available")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        def fetch_certificates():
            try:
                certificates = list(collection.find({}))
                # Sort by created_at (newest added first), then by completion date
                def sort_key(x):
                    created = x.get("created_at")
                    if created is not None and hasattr(created, "timestamp"):
                        return (created.timestamp(), x.get("completion_year", 0), x.get("completion_month", 0))
                    return (0, x.get("completion_year", 0), x.get("completion_month", 0))
                certificates.sort(key=sort_key, reverse=True)
                result = []
                for cert in certificates:
                    try:
                        converted = convert_objectid_to_str(cert)
                        result.append(converted)
                    except Exception as e:
                        print(f"[WARNING] Failed to convert certificate {cert.get('_id', 'unknown')}: {e}")
                        converted = cert.copy() if cert else {}
                        if "_id" in converted:
                            converted["id"] = str(converted["_id"])
                            del converted["_id"]
                        if "created_at" in converted:
                            if isinstance(converted["created_at"], datetime):
                                converted["created_at"] = converted["created_at"].isoformat()
                        result.append(converted)
                return result
            except Exception as e:
                print(f"[ERROR] Error in fetch_certificates: {e}")
                import traceback
                traceback.print_exc()
                raise
        
        certificates = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_certificates
        )
        print(f"[INFO] Successfully fetched {len(certificates)} certificates")
        return certificates
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Failed to fetch certificates: {error_msg}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch certificates: {error_msg}"
        )


@router.get("/certificates/{certificate_id}")
async def get_certificate(certificate_id: str):
    """
    Get a single certificate by ID.
    """
    try:
        collection = get_certificates_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        try:
            object_id = ObjectId(certificate_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid certificate ID format"
            )
        
        def fetch_certificate():
            certificate = collection.find_one({"_id": object_id})
            return convert_objectid_to_str(certificate) if certificate else None
        
        certificate = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_certificate
        )
        
        if certificate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certificate not found"
            )
        
        return certificate
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to fetch certificate: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch certificate: {str(e)}"
        )


@router.post("/certificates", status_code=status.HTTP_201_CREATED)
async def create_certificate(
    certificate: CertificateCreate,
    admin: bool = Depends(verify_admin_password)
):
    """
    Create a new certificate.
    Requires admin authentication.
    """
    try:
        collection = get_certificates_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        try:
            certificate_dict = certificate.model_dump()
            print(f"[INFO] Creating certificate: {certificate_dict.get('title')}")
        except Exception as e:
            print(f"[ERROR] Validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Validation error: {str(e)}"
            )
        
        certificate_dict["created_at"] = datetime.now(timezone.utc)
        
        def insert_certificate():
            try:
                result = collection.insert_one(certificate_dict)
                return str(result.inserted_id)
            except Exception as e:
                print(f"[ERROR] MongoDB insert error: {e}")
                import traceback
                traceback.print_exc()
                raise
        
        cert_id = await asyncio.get_event_loop().run_in_executor(
            executor,
            insert_certificate
        )
        
        def fetch_new_certificate():
            try:
                cert = collection.find_one({"_id": ObjectId(cert_id)})
                if cert:
                    return convert_objectid_to_str(cert)
                return None
            except Exception as e:
                print(f"[ERROR] Error fetching new certificate: {e}")
                return None
        
        new_certificate = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_new_certificate
        )
        
        if new_certificate is None:
            return {
                "message": "Certificate created successfully",
                "certificate_id": cert_id
            }
        
        return {
            "message": "Certificate created successfully",
            "certificate": new_certificate
        }
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Failed to create certificate: {error_msg}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create certificate: {error_msg}"
        )


@router.put("/certificates/{certificate_id}")
async def update_certificate(
    certificate_id: str,
    certificate_update: CertificateUpdate,
    admin: bool = Depends(verify_admin_password)
):
    """
    Update an existing certificate.
    Requires admin authentication.
    """
    try:
        collection = get_certificates_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        try:
            object_id = ObjectId(certificate_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid certificate ID format"
            )
        
        update_data = certificate_update.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        def update_certificate():
            result = collection.update_one(
                {"_id": object_id},
                {"$set": update_data}
            )
            return result.modified_count > 0
        
        updated = await asyncio.get_event_loop().run_in_executor(
            executor,
            update_certificate
        )
        
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certificate not found"
            )
        
        def fetch_updated_certificate():
            cert = collection.find_one({"_id": object_id})
            return convert_objectid_to_str(cert) if cert else None
        
        updated_certificate = await asyncio.get_event_loop().run_in_executor(
            executor,
            fetch_updated_certificate
        )
        
        return {
            "message": "Certificate updated successfully",
            "certificate": updated_certificate
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to update certificate: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update certificate: {str(e)}"
        )


@router.delete("/certificates/{certificate_id}")
async def delete_certificate(
    certificate_id: str,
    admin: bool = Depends(verify_admin_password)
):
    """
    Delete a certificate.
    Requires admin authentication.
    """
    try:
        collection = get_certificates_collection()
        if collection is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not available"
            )
        
        try:
            object_id = ObjectId(certificate_id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid certificate ID format"
            )
        
        def delete_certificate():
            result = collection.delete_one({"_id": object_id})
            return result.deleted_count > 0
        
        deleted = await asyncio.get_event_loop().run_in_executor(
            executor,
            delete_certificate
        )
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certificate not found"
            )
        
        return {
            "message": "Certificate deleted successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to delete certificate: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete certificate: {str(e)}"
        )


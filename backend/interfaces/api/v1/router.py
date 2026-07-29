"""API v1 router aggregation."""

from fastapi import APIRouter

from backend.interfaces.api.v1.ai import router as ai_router
from backend.interfaces.api.v1.assessments import router as assessments_router
from backend.interfaces.api.v1.auth import router as auth_router
from backend.interfaces.api.v1.findings import router as findings_router
from backend.interfaces.api.v1.plugins import router as plugins_router
from backend.interfaces.api.v1.projects import router as projects_router
from backend.interfaces.api.v1.reports import router as reports_router
from backend.interfaces.api.v1.scans import router as scans_router
from backend.interfaces.api.v1.pipeline import router as pipeline_router
from backend.interfaces.api.v1.users import router as users_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(users_router, prefix="/users", tags=["Users"])
api_v1_router.include_router(projects_router, prefix="/projects", tags=["Projects"])
api_v1_router.include_router(assessments_router, prefix="/assessments", tags=["Assessments"])
api_v1_router.include_router(findings_router, prefix="/findings", tags=["Findings"])
api_v1_router.include_router(reports_router, prefix="/reports", tags=["Reports"])
api_v1_router.include_router(ai_router, prefix="/ai", tags=["AI"])
api_v1_router.include_router(plugins_router, prefix="/plugins", tags=["Plugins"])
api_v1_router.include_router(scans_router, prefix="/scans", tags=["Scans"])
api_v1_router.include_router(pipeline_router, prefix="/pipeline", tags=["Pipeline"])

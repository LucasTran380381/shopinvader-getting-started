# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from fastapi import APIRouter, FastAPI
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.middleware.cors import CORSMiddleware

from odoo import api, fields, models

from odoo.addons.shopinvader_api_settings.routers import settings_router
from odoo.addons.shopinvader_api_cart.routers import cart_router
from odoo.addons.shopinvader_api_customer.routers import customer_router
from odoo.addons.fastapi.dependencies import authenticated_partner_impl
from odoo.addons.shopinvader_fastapi_auth_jwt.dependencies import (
    auth_jwt_authenticated_or_anonymous_partner,
    auth_jwt_authenticated_or_anonymous_partner_autocreate,
)
from odoo.addons.shopinvader_api_signin_jwt.routers import signin_router

class FastapiEndpoint(models.Model):
    _inherit = "fastapi.endpoint"

    app: str = fields.Selection(
        selection_add=[("shopinvader_demo", "Shopinvader Trobz Demo Endpoint")],
        ondelete={"shopinvader_demo": "cascade"},
    )
    auth_jwt_validator_id = fields.Many2one("auth.jwt.validator")

    def _get_app_dependencies_overrides(self):
        dependencies = super()._get_app_dependencies_overrides()
        dependencies.update({
            authenticated_partner_impl: auth_jwt_authenticated_or_anonymous_partner_autocreate
        })
        return dependencies

    def _get_app(self):
        app = super()._get_app()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Specify your frontend URL in production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        app.include_router(settings_router)
        app.include_router(signin_router)
        app.include_router(customer_router)
        app.include_router(cart_router, prefix="/carts")
        return app

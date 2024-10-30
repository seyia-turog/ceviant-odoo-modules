from odoo import http
from odoo.http import request, Response
from werkzeug.wrappers import Response
from ..models.validation import validate_account_entry
from ..models.account_utils import create_account, get_account_records, get_account_data
import logging
import json
from ..models.rabbitmq_publisher import generate_batch_reference

_logger = logging.getLogger(__name__)


class AccountEntryController(http.Controller):
    @http.route('/ledger/accounts', type='http', auth='public', methods=['POST'], csrf=False)
    def handle_account(self):
        raw_data = request.httprequest.data.decode('utf-8')

        try:
            payload = json.loads(raw_data)
            _logger.info("Received payload: %s", json.dumps(payload))
        except json.JSONDecodeError as e:
            _logger.error("Invalid JSON payload: %s", e)
            return Response(
                json.dumps({
                    "code": 400,
                    "status": "error",
                    "data": {"message": "Invalid JSON payload", "responseId": None}
                }),
                status=400,
                content_type='application/json'
            )

        valid, error = validate_account_entry(payload)
        if not valid:
            return Response(
                json.dumps({
                    "code": 400,
                    "status": "error",
                    "data": {"message": error, "responseId": None}
                }),
                status=400,
                content_type='application/json'
            )

        try:
            response = create_account(payload)
            return response
        except Exception as e:
            _logger.error("Failed to process account request: %s", e)
            return Response(
                json.dumps({
                    "code": 500,
                    "status": "error",
                    "data": {"message": "Failed to process account request.", "responseId": None}
                }),
                status=500,
                content_type='application/json'
            )

    @http.route('/ledger/accounts', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all_accounts_api(self, **kwargs):
        accounts = get_account_records(request.env)
        account_data = get_account_data(request.env, accounts)
        _logger.info(f"Account data: {account_data}")

        response = {
            'code': 200,
            'status': 'success',
            'data': account_data
        }
        return json.dumps(response)

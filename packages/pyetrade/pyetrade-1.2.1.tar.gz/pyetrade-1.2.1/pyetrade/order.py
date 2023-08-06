"""Order - ETrade Order API

   TODO:
       * Preview equity order change
       * Place equity order change
       * Preview option order
       * Place option order
       * Preview option order change
       * Place option order change

"""

import logging
import jxmlease
from requests_oauthlib import OAuth1Session

LOGGER = logging.getLogger(__name__)


class OrderException(Exception):
    """:description: Exception raised when giving bad args to a method not from Etrade calls

    """

    def __init__(self, explanation=None, params=None):
        super().__init__()
        self.required = params
        self.args = (explanation, params)

    def __str__(self):
        return "Missing required parameters"


class ETradeOrder:
    """:description: Object to perform Orders

       :param client_key: Client key provided by Etrade
       :type client_key: str, required
       :param client_secret: Client secret provided by Etrade
       :type client_secret: str, required
       :param resource_owner_key: Resource key from :class:`pyetrade.authorization.ETradeOAuth`
       :type resource_owner_key: str, required
       :param resource_owner_secret: Resource secret from
            :class:`pyetrade.authorization.ETradeOAuth`
       :type resource_owner_secret: str, required
       :param dev: Defines Sandbox (True) or Live (False) ETrade, defaults to True
       :type dev: bool, optional
       :param timeout: Timeout value for OAuth, defaults to 30
       :type timeout: int, optional
       :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

    """

    def __init__(
        self,
        client_key,
        client_secret,
        resource_owner_key,
        resource_owner_secret,
        dev=True,
        timeout=30,
    ):
        self.base_url = (
            r"https://apisb.etrade.com/v1/accounts"
            if dev
            else r"https://api.etrade.com/v1/accounts"
        )
        self.dev_environment = dev
        self.timeout = timeout
        self.session = OAuth1Session(
            client_key,
            client_secret,
            resource_owner_key,
            resource_owner_secret,
            signature_type="AUTH_HEADER",
        )

    def list_orders(self, account_id, resp_format="json", **kwargs):
        """:description: Lists orders for a specific account ID Key

        :param account_id: AccountIDKey from :class:`pyetrade.accounts.ETradeAccounts.list_accounts`
        :type  account_id: str, required
        :param resp_format: Desired Response format, defaults to xml
        :type  resp_format: str, optional
        :param kwargs: Parameters for api. Refer to EtradeRef for options
        :type  kwargs: ``**kwargs``, optional
        :return: List of orders for an account
        :rtype: ``xml`` or ``json`` based on ``resp_format``
        :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

        """
        assert resp_format in ("json", "xml")
        api_url = self.base_url + "/" + account_id + "/orders"
        if resp_format == "json":
            api_url += ".json"

        # Build Params
        params = kwargs
        LOGGER.debug("query string params: %s", params)

        LOGGER.debug(api_url)
        req = self.session.get(api_url, params=params, timeout=self.timeout)
        LOGGER.debug(req.text)
        req.raise_for_status()

        if resp_format == "json":
            return req.json()
        return req.text

    def check_order(self, **kwargs):
        """:description: Check that required params for preview or place order are there and correct

                         (Used internally)

        """
        mandatory = [
            "accountId",
            "symbol",
            "orderAction",
            "clientOrderId",
            "priceType",
            "quantity",
            "orderTerm",
            "marketSession",
        ]
        if not all(param in kwargs for param in mandatory):
            raise OrderException

        if kwargs["priceType"] == "STOP" and "stopPrice" not in kwargs:
            raise OrderException
        if kwargs["priceType"] == "LIMIT" and "limitPrice" not in kwargs:
            raise OrderException
        if (
            kwargs["priceType"] == "STOP_LIMIT"
            and "limitPrice" not in kwargs
            and "stopPrice" not in kwargs
        ):
            raise OrderException

    def build_order_payload(self, order_type, **kwargs):
        """:description: Builds the POST payload of a preview or place order
                         (Used internally)

           :param order_type: PreviewOrderRequest or PlaceOrderRequest
           :type  order_type: str, required
           :return: Builds Order Payload
           :rtype: ``xml`` or ``json`` based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

        """
        instrument = {
            "Product": {"securityType": "EQ", "symbol": kwargs["symbol"]},
            "orderAction": kwargs["orderAction"],
            "quantityType": "QUANTITY",
            "quantity": kwargs["quantity"],
        }
        order = kwargs
        order["Instrument"] = instrument
        order["stopPrice"] = ""
        payload = {
            order_type: {
                "orderType": "EQ",
                "clientOrderId": kwargs["clientOrderId"],
                "Order": order,
            }
        }

        if "previewId" in kwargs:
            payload[order_type]["PreviewIds"] = {"previewId": kwargs["previewId"]}

        return payload

    def perform_request(self, method, resp_format, api_url, payload):
        """:description: POST or PUT request with json or xml used by preview, place and cancel

           :param method: PUT or POST method
           :type method: session, required
           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, required
           :param api_url: API URL
           :type  api_url: str, required
           :param payload: Payload
           :type  payload: str[], required
           :return: Return request
           :rtype: xml or json based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

        """

        LOGGER.debug(api_url)
        LOGGER.debug("payload: %s", payload)
        if resp_format == "json":
            req = method(api_url, json=payload, timeout=self.timeout)
        else:
            headers = {"Content-Type": "application/xml"}
            payload = jxmlease.emit_xml(payload)
            LOGGER.debug("xml payload: %s", payload)
            req = method(api_url, data=payload, headers=headers, timeout=self.timeout)

        LOGGER.debug(req.text)
        req.raise_for_status()

        if resp_format == "json":
            return req.json()
        if resp_format is None:
            return jxmlease.parse(req.text)
        return req.text

    def preview_equity_order(self, resp_format=None, **kwargs):
        """API is used to submit an order request for preview before placing it

           :param resp_format: Desired Response format (json or xml), defaults to xml
           :type  resp_format: str, optional
           :param accountId: AccountIDkey retrived from :class:`list_accounts`
           :type  accountId: str, required
           :param symbol: Market symbol for the security being bought or sold
           :type  symbol: str, required
           :param orderAction: Action that the broker is requested to perform
           :type  orderAction: str, required
           :orderAction values:
               * BUY
               * SELL
               * BUY_TO_COVER
               * SELL_SHORT
           :param previewId: Required only if order was previewed.
                             Numeric preview ID from preview.
                             **Note** - Other parameters much match that of preview
           :type  previewId: long, conditional
           :param clientOrderId: Reference number generated by developer.
                                 Used to ensure duplicate order is not submitted.
                                 Value can be of 20 alphanmeric characters or less
                                 Must be uniquewithin this account.
                                 Does not appear in any API responses.
           :type  clientOrderId: str, required
           :param priceType: Type of pricing specified in equity order
           :type  priceType: str, required
           :priceType values:
               * MARKET
               * LIMIT - Requires `limitPrice`
               * STOP - Requires `stopPrice`
               * STOP_LIMIT - Requires `limitPrice`
               * MARKET_ON_CLOSE
           :param limitPrice: Highest to buy or lowest to sell.
                              Required if `priceType` is `STOP` or `STOP_LIMIT`
           :type  limitPrice: double, conditional
           :param stopPrice: Price to buy or sell if specified in a stop order.
                             Required if `priceType` is  `STOP` or `STOP_LIMIT`
           :type  stopPrice: double, conditional
           :param allOrNone: Specifies if order must be executed all at once.
                             TRUE triggers `allOrNone`, defaults to FALSE
           :type  allOrNone: bool, optional
           :param quantity: Number of shares to buy or sell
           :type  quantity: int, required
           :param reserveOrder: If set to TRUE, publicly displays only a limited
                                number of shares (the reserve quantity), instead
                                of the entire order, to avoid influencing other
                                traders. If TRUE, must also specify the
                                `reserveQuantity`, defaults to FALSE
           :type  reserveOrder: bool, optional
           :param reserveQuantity: Number of shares to be publicly displayed if
                                   this is a reserve order. Required if
                                   `reserveOrder` is TRUE.
           :type reserveQuantity: int, conditional
           :param marketSession: Session to place the equity order
           :type  marketSession: str, required
           :marketSession values:
               * REGULAR
               * EXTENDED
           :param orderTerm: Term for which the order is in effect.
           :type  orderTerm: str, required
           :orderTerm values:
               * GOOD_UNTIL_CANCEL
               * GOOD_FOR_DAY
               * IMMEDIATE_OR_CANCEL (only for `LIMIT` orders)
               * FILL_OR_KILL (only for `LIMIT` orders)
           :param routingDestination: Exchange where the order should be executed.
           :type  routingDestination: str, optional
           :routingDestination values:
               * AUTO (default)
               * ARCA
               * NSDQ
               * NYSE
           :param estimatedCommission: Cost billed to the user to preform requested action
           :type  estimatedCommission: double
           :param estimatedTotalAmount: Cost including commission
           :type  estimatedTotalAmount: double
           :param messageList: Container for messages describing the result of the action
           :type  messageList: dict
           :param msgDesc: Text of the result message, indicating order status, success
                           or failure, additional requirements that must be met before
                           placing the order, etc. Applications typically display this
                           message to the user, which may result in further user action
           :type  msgDesc: str
           :param msgCode: Standard numeric code of the result message. Refer to
                           the Error Messages documentation for examples. May optionally
                           be displayed to the user, but is primarily intended for
                           internal use.
           :type  msgCode: int
           :param orderNum: Numeric ID for this order in the E*TRADE system
           :type  orderNum: int
           :param orderTime: The epoch time the order was submitted.
           :type  orderTime: long
           :param symbolDesc: Text description of the security
           :type  symbolDesc: str
           :param symbol: The market symbol for the underlier
           :type  symbol: str
           :return: Confirmation of the Preview Equity Order
           :rtype: ``xml`` or ``json`` based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

        """
        assert resp_format in (None, "json", "xml")
        LOGGER.debug(kwargs)

        # Test required values
        self.check_order(**kwargs)

        api_url = self.base_url + "/" + kwargs["accountId"] + "/orders/preview"
        # payload creation
        payload = self.build_order_payload("PreviewOrderRequest", **kwargs)

        return self.perform_request(self.session.post, resp_format, api_url, payload)

    def change_preview_equity_order(self, resp_format=None, **kwargs):
        """:description: Same as :class:`preview_equity_order` with orderId
           :param orderId: orderId to modify, refer :class:`list_orders`
           :type  orderId: str, required
           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, optional
           :param accountId: AccountIDkey retrived from :class:`list_accounts`
           :type  accountId: str, required
           :return: Previews Changed order with orderId for account with key accountId
           :rtype: xml or json based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

        """
        assert resp_format in (None, "json", "xml")
        LOGGER.debug(kwargs)

        # Test required values
        self.check_order(**kwargs)

        api_url = self.base_url + "/" + kwargs["accountId"] + "/orders/"+kwargs["orderId"]+"/change/preview"
        # payload creation
        payload = self.build_order_payload("PreviewOrderRequest", **kwargs)

        return self.perform_request(self.session.put, resp_format, api_url, payload)

    def place_equity_order(self, resp_format=None, **kwargs):
        """:description: Places Equity Order

           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, optional
           :param kwargs: Parameters for api, refer :class:`change_preview_equity_order`
           :type  kwargs: ``**kwargs``, required
           :return: Returns confirmation of the equity order
           :rtype: xml or json based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

        """

        assert resp_format in (None, "json", "xml")
        LOGGER.debug(kwargs)

        # Test required values
        self.check_order(**kwargs)

        if "previewId" not in kwargs:
            LOGGER.debug(
                "No previewId given, previewing before placing order "
                "because of an Etrade bug as of 1/1/2019"
            )
            preview = self.preview_equity_order(resp_format, **kwargs)
            if resp_format == "xml":
                preview = jxmlease.parse(preview)
            kwargs["previewId"] = preview["PreviewOrderResponse"]["PreviewIds"][
                "previewId"
            ]
            LOGGER.debug(
                "Got a successful preview with previewId: %s", kwargs["previewId"]
            )

        api_url = self.base_url + "/" + kwargs["accountId"] + "/orders/place"
        # payload creation
        payload = self.build_order_payload("PlaceOrderRequest", **kwargs)

        return self.perform_request(self.session.post, resp_format, api_url, payload)

    def place_changed_equity_order(self, resp_format=None, **kwargs):
        """:description: Places changes to equity orders

           :param resp_format: Desired Response format, defaults to xml
           :type  resp_format: str, optional
           :param kwargs: Parameters for api, refer :class:`change_preview_equity_order`
           :type  kwargs: ``**kwargs``, required
           :return: Returns confirmation similar to :class:`preview_equity_order`
           :rtype: xml or json based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

        """

        assert resp_format in (None, "json", "xml")
        LOGGER.debug(kwargs)

        # Test required values
        self.check_order(**kwargs)

        if "previewId" not in kwargs:
            LOGGER.debug(
                "No previewId given, previewing before placing order "
                "because of an Etrade bug as of 1/1/2019"
            )
            preview = self.preview_equity_order(resp_format, **kwargs)
            if resp_format == "xml":
                preview = jxmlease.parse(preview)
            kwargs["previewId"] = preview["PreviewOrderResponse"]["PreviewIds"][
                "previewId"
            ]
            LOGGER.debug(
                "Got a successful preview with previewId: %s", kwargs["previewId"]
            )

        api_url = self.base_url + "/" + kwargs["accountId"] + "/orders/"+kwargs["orderId"]+"change/place"
        # payload creation
        payload = self.build_order_payload("PlaceOrderRequest", **kwargs)

        return self.perform_request(self.session.put, resp_format, api_url, payload)

    def cancel_order(self, account_id, order_num, resp_format=None):
        """:description: Cancels a specific order for a given account

           :param account_id: AccountIDkey retrived from
                              :class:`pyetrade.accounts.ETradeAccounts.list_accounts`
           :type  account_id: str, required
           :param order_num: Numeric id for this order listed in :class:`list_orders`
           :type  order_num: int, required
           :param resp_format: Desired Response format("None", "json", "xml"), defaults to xml
           :type  resp_format: str, optional
           :return: Confirmation of cancellation
           :rtype: ``xml`` or ``json`` based on ``resp_format``
           :EtradeRef: https://apisb.etrade.com/docs/api/order/api-order-v1.html

        """
        assert resp_format in (None, "json", "xml")
        api_url = self.base_url + "/" + account_id + "/orders/cancel"
        payload = {"CancelOrderRequest": {"orderId": order_num}}

        return self.perform_request(self.session.put, resp_format, api_url, payload)

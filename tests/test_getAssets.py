from backend.getAssets import GetAssets, calculateTotal, calculateGainLossPercentage, calculateGainLoss, sortByTotal

import math
import json
import unittest
from unittest.mock import MagicMock, patch



def test_calculateTotal():
    assert calculateTotal(10, 10) == 100
    assert calculateTotal(2, 3.3) == 6.6
    assert calculateTotal(-2, 8) == -16
    assert calculateTotal(-3, -5) == 15

def test_calculateGainLoss():
    assert calculateGainLoss(15, 10, 1) == 5
    assert calculateGainLoss(10, 15, 2) == -10
    assert calculateGainLoss(10, 0, 2) == 20
    assert calculateGainLoss(0, 15, 4) == -60
    assert calculateGainLoss(0, 0, 4) == 0

def test_calculateGainLossPercentage():
    assert math.isclose(calculateGainLossPercentage(11, 10), 10)
    assert math.isclose(calculateGainLossPercentage(9, 10), -10)
    assert math.isclose(calculateGainLossPercentage(10, 10), 0)

def test_sortByTotal():
        asset_list = [
            {"total": "$100.00"},
            {"total": "$300.00"},
            {"total": "$200.00"}
        ]

        sorted_list = sorted(asset_list, key=sortByTotal, reverse=True)

        unittest.TestCase().assertEqual(first=sorted_list, second=[
            {"total": "$300.00"},
            {"total": "$200.00"},
            {"total": "$100.00"}
        ])

@patch('backend.getAssets.Database')
@patch('backend.getAssets.yf.Ticker')
def test_respond(MockTicker, MockDatabase):
    # Mock request handler
    request_handler = MagicMock()
    request_handler.authenticator.getUserIdAndAuthKeyFromCookies.return_value = (1, 'auth_key')
    
    # Mock database
    db_instance = MockDatabase.return_value
    db_instance.getAssets.return_value = [
        ("stock(US)", "META", 10, 20.0),
        ("stock(US)", "AAPL", 5, 150.0)
    ]

    # Mock yfinance Ticker
    ticker_instance = MockTicker.return_value
    ticker_instance.fast_info = {"lastPrice": 30.0}

    # Initialize GetAssets and call respond method
    get_assets = GetAssets(request_handler)
    get_assets.respond()

    # Validate response
    expected_response = [
        {
            "type": "stock(US)",
            "asset": "META",
            "quantity": 10,
            "avg_price": "$20.00",
            "gain_loss": "$100.00",
            "gain_loss_percent": "50.00%",
            "total": "$300.00",
        },
        {
            "type": "stock(US)",
            "asset": "AAPL",
            "quantity": 5,
            "avg_price": "$150.00",
            "gain_loss": "$-600.00",
            "gain_loss_percent": "-80.00%",
            "total": "$150.00",
        }
    ]

    # Check send_response call
    request_handler.send_response.assert_called_once_with(200, "OK")
    request_handler.send_header.assert_called_once_with('Content-type', 'application/json')
    request_handler.end_headers.assert_called_once()

    # Check wfile write call
    request_handler.wfile.write.assert_called_once_with(json.dumps(expected_response).encode('utf-8'))

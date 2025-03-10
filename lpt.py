from playwright.sync_api import sync_playwright
import pytest

# Test Data
VALID_USER = "testuser"
VALID_PASSWORD = "password123"
FRAUD_LIMIT = 10000  # Any transaction above this is flagged


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


def test_login(browser):
    page = browser.new_page()
    page.goto("http://localhost:8000/login.html")  # Local banking app
    
    page.fill("#username", VALID_USER)
    page.fill("#password", VALID_PASSWORD)
    page.click("#login")
    
    assert "Welcome" in page.inner_text("#status")
    page.close()


def test_fund_transfer(browser):
    page = browser.new_page()
    page.goto("http://localhost:8000/transfer.html")
    
    page.fill("#amount", "500")
    page.fill("#recipient", "JohnDoe")
    page.click("#transfer")
    
    assert "Transfer Successful" in page.inner_text("#status")
    page.close()


def test_fraud_detection(browser):
    page = browser.new_page()
    page.goto("http://localhost:8000/transfer.html")
    
    page.fill("#amount", str(FRAUD_LIMIT + 1))  # Enter an amount above the fraud limit
    page.fill("#recipient", "Hacker")
    page.click("#transfer")
    
    assert "Transaction Blocked! Fraud Alert!" in page.inner_text("#status")
    page.close()


if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html"])  # Generate a test report



# Test-Automation-Banking
I have implemented an automated test suite using Playwright and Pytest for a local banking application. The tests cover:
User Login
Fund Transfers
Fraud Detection (Blocking transactions above a defined limit)

**Code Explanation:**
**1. Test Data & Setup**
VALID_USER = "testuser"
VALID_PASSWORD = "password123"
FRAUD_LIMIT = 10000  # Any transaction above this is flagged

Defines test credentials and a fraud detection limit.

**2. Browser Fixture (Reusable Browser Instance)**
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Runs with UI
        yield browser  # Keeps browser open for all tests
        browser.close()  # Closes after tests

-Initializes a Chromium browser using Playwright.
-Runs in non-headless mode for debugging.
-Ensures browser cleanup after all tests.

**3. Test 1: User Login**
def test_login(browser):
    page = browser.new_page()
    page.goto("http://localhost:8000/login.html")  # Local banking app
    
    page.fill("#username", VALID_USER)
    page.fill("#password", VALID_PASSWORD)
    page.click("#login")
    
    assert "Welcome" in page.inner_text("#status")
    page.close()

-Navigates to the login page.
-Fills in the username and password fields.
-Clicks the login button.
-Asserts the presence of "Welcome" in the page status to confirm login success.

**4. Test 2: Fund Transfer**
def test_fund_transfer(browser):
    page = browser.new_page()
    page.goto("http://localhost:8000/transfer.html")
    
    page.fill("#amount", "500")
    page.fill("#recipient", "JohnDoe")
    page.click("#transfer")
    
    assert "Transfer Successful" in page.inner_text("#status")
    page.close()

-Navigates to the fund transfer page.
-Inputs an amount (500) and recipient (JohnDoe).
-Clicks the transfer button.
-Confirms success message "Transfer Successful".

**5. Test 3: Fraud Detection (Blocking High-Value Transactions)**
def test_fraud_detection(browser):
    page = browser.new_page()
    page.goto("http://localhost:8000/transfer.html")
    
    page.fill("#amount", str(FRAUD_LIMIT + 1))  # Enter an amount above the fraud limit
    page.fill("#recipient", "Hacker")
    page.click("#transfer")
    
    assert "Transaction Blocked! Fraud Alert!" in page.inner_text("#status")
    page.close()

-Attempts a high-value transaction (above FRAUD_LIMIT).
-Checks if the system blocks the transaction and shows a fraud alert.

**6. Running Tests & Generating a Report**

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html"])  # Generate a test report

-Runs the tests in verbose mode.
-Generates an HTML test report (report.html).



















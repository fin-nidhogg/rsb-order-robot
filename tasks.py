from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
import shutil

@task
def order_robot_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(slowmo=200)
    open_robot_order_website()
    download_order_data()
    process_orders_from_csv()
    create_archive()
    clean_up_temp_files()

def open_robot_order_website():
    """Opens the robot ordering page and accepts the initial popup."""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    page = browser.page()
    page.click('text=OK')

def download_order_data():
    """Downloads the CSV file containing robot order data."""
    http = HTTP()
    http.download("https://robotsparebinindustries.com/orders.csv", overwrite=True)

def process_orders_from_csv():
    """Reads order data from CSV and processes each order entry."""
    csv_handler = Tables()
    orders = csv_handler.read_table_from_csv("orders.csv")
    for order in orders:
        fill_and_submit_order_form(order)

def fill_and_submit_order_form(order):
    """Fills in and submits the robot order form with data from an order entry."""
    page = browser.page()
    select_robot_head(order["Head"])
    select_robot_body(order["Body"])
    enter_order_details(order["Legs"], order["Address"])
    submit_order_form(order)

def select_robot_head(head_number):
    """Selects the robot head based on the provided head number."""
    head_options = {
        "1": "Roll-a-thor head",
        "2": "Peanut crusher head",
        "3": "D.A.V.E head",
        "4": "Andy Roid head",
        "5": "Spanner mate head",
        "6": "Drillbit 2000 head"
    }
    page = browser.page()
    page.select_option("#head", head_options.get(head_number))

def select_robot_body(body_number):
    """Selects the robot body based on the provided body number."""
    page = browser.page()
    page.click(f'//*[@id="root"]/div/div[1]/div/div[1]/form/div[2]/div/div[{body_number}]/label')

def enter_order_details(legs, address):
    """Fills in the legs part number and delivery address in the form."""
    page = browser.page()
    page.fill("input[placeholder='Enter the part number for the legs']", legs)
    page.fill("#address", address)

def submit_order_form(order):
    """Submits the order form, saves receipt as PDF, takes a screenshot, and embeds it.
       Retries if the 'Order another' button is not available due to a random error."""
    page = browser.page()
    max_retries = 5  # Maximum number of retries for clicking 'Order'
    retries = 0

    while retries < max_retries:
        page.click("#order")
        
        # Check if the 'Order another' button appears, signaling successful order submission
        if page.query_selector("#order-another"):
            pdf_path = save_receipt_as_pdf(order["Order number"])
            screenshot_path = capture_robot_screenshot(order["Order number"])
            add_screenshot_to_receipt(screenshot_path, pdf_path)
            order_another_robot()
            acknowledge_popup()
            break  # Exit the loop as the order was successfully placed

        retries += 1
        print(f"Retrying to submit order... Attempt {retries}")

    else:
        print("Failed to submit the order after multiple attempts.")

def save_receipt_as_pdf(order_number):
    """Saves the order receipt as a PDF file."""
    page = browser.page()
    receipt_html = page.locator("#receipt").inner_html()
    pdf_path = f"output/receipts/{order_number}.pdf"
    pdf = PDF()
    pdf.html_to_pdf(receipt_html, pdf_path)
    return pdf_path

def capture_robot_screenshot(order_number):
    """Captures a screenshot of the ordered robot and saves it as a PNG file."""
    page = browser.page()
    screenshot_path = f"output/screenshots/{order_number}.png"
    page.locator("#robot-preview-image").screenshot(path=screenshot_path)
    return screenshot_path

def add_screenshot_to_receipt(screenshot_path, pdf_path):
    """Embeds the screenshot of the robot into the PDF receipt."""
    pdf = PDF()
    pdf.add_watermark_image_to_pdf(image_path=screenshot_path, 
                                   source_path=pdf_path, 
                                   output_path=pdf_path)

def order_another_robot():
    """Initiates the process to order another robot."""
    page = browser.page()
    page.click("#order-another")

def acknowledge_popup():
    """Acknowledges the popup message after placing each order."""
    page = browser.page()
    page.click('text=OK')

def create_archive():
    """Creates a ZIP archive containing all PDF receipts and screenshots."""
    archive = Archive()
    archive.archive_folder_with_zip("./output/receipts", "./output/receipts.zip")

def clean_up_temp_files():
    """Removes temporary files and folders created during the process."""
    shutil.rmtree("./output/receipts")
    shutil.rmtree("./output/screenshots")

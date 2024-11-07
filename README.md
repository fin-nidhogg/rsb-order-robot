# Robot Order Automation Project

This project was developed as part of the requirements for **Robocorp's Automation Certification Level II: Build a Robot**. It automates the process of ordering robots from **RobotSpareBin Industries Inc.**, including form submission, receipt generation, and archiving.

## Project Overview

- **Automated Ordering**: Reads order data from a CSV file and submits it on the website.
- **PDF Receipts**: Saves order receipts as PDF files.
- **Screenshot Capture**: Takes and embeds screenshots of each ordered robot in the receipts.
- **Archiving**: Packages all receipts and screenshots into a ZIP file.

## Technologies Used

- **Robocorp** tools and libraries for task automation
- **RPA.Browser** for web interactions
- **RPA.HTTP** and **RPA.Tables** for file management
- **RPA.PDF** for PDF creation
- **RPA.Archive** for creating ZIP files

## Getting Started

1. Clone this repository and install the dependencies listed in `requirements.txt`.
2. Run the automation script with Robocorp Lab or a compatible environment.

For full instructions and details, refer to the [official Robocorp documentation](https://robocorp.com/docs/).

## License

This project is licensed under the MIT License.

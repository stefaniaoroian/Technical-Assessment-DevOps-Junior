import requests
from datetime import datetime
import pandas as pd

class LicenseAuthority:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, num_points):
        try:
            response = requests.get(f"{self.api_url}?limit={num_points}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch data from API. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred while fetching data: {e}")
            return None

    def list_suspended_licenses(self, data):
        print("Original data length:", len(data))
        suspended_licenses = [license for license in data if license.get("suspendat") == True]
        print("Filtered data length:", len(suspended_licenses))
        return suspended_licenses

    def extract_valid_licenses(self, data):
        today = datetime.today().strftime("%d-%m-%Y")
        valid_licenses = []
        for license in data:
            # Parse the expiration date string into a datetime object
            exp_date_str = license["dataDeExpirare"]
            try:
                exp_date = datetime.strptime(exp_date_str, "%d/%m/%Y")
            except ValueError:
                print(f"Invalid date format: {exp_date_str}")
                continue

            # Compare the expiration date with today's date
            if exp_date >= datetime.today():
                valid_licenses.append(license)
        return valid_licenses

    def find_license_count_by_category(self, data):
        license_count = {}
        for license in data:
            category = license["categorie"]
            license_count[category] = license_count.get(category, 0) + 1
        return license_count

    def run_operation(self, operation_id, num_points):
        data = self.fetch_data(num_points)
        if data:
            if operation_id == 1:
                result = self.list_suspended_licenses(data)
            elif operation_id == 2:
                result = self.extract_valid_licenses(data)
            elif operation_id == 3:
                result = self.find_license_count_by_category(data)
            else:
                print("Invalid operation ID. Please choose 1, 2, or 3.")
                return None
            return result
        else:
            return None
        
    def generate_excel_file(self, data, file_path):
        if data:
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)
            print(f"Excel file generated successfully: {file_path}")
        else:
            print("No data to generate Excel file.")


def main():
    api_url = "http://localhost:30000/drivers-licenses/list"
    authority = LicenseAuthority(api_url)
    num_points = 150

    operation_id = int(input("Enter the operation ID (1, 2, or 3): "))
    result = authority.run_operation(operation_id, num_points)
    if result is not None:
        print("Operation completed successfully.")
        file_path = "C:/Users/steff/Desktop/DevOps/output.xlsx" 
        authority.generate_excel_file(result, file_path)
    else:
        print("Failed to fetch and process data. Please check the API or try again later.")

if __name__ == "__main__":
    main()

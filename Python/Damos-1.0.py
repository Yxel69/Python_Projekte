import sys
import os
import csv
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QMessageBox,
    QDialog,
    QListWidget,
    QCheckBox,
    QFileDialog,
)

from PyQt6.QtGui import QIcon

os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Datenbankeingabe")
        self.setWindowIcon(QIcon("pikachu.png"))
        self.main_layout = QVBoxLayout()

        # Initialize input fields and entry storage
        self.input_fields = []
        self.checkboxes = []  # To store checkboxes for selection
        self.all_entries = {}  # Store all saved entries with Firmenname as key
        self.current_entry_key = None  # Track the currently selected entry key

        fields = [
            "Firmenname:",
            "Handelsregister:",  # This will be used as the key
            "Straßenname:",
            "Hausnummer:",
            "PLZ:",
            "Ort:",
            "Anrede:",
            "AP_Vorname:",
            "AP_Nachname:"
        ]

        # Create input fields and associated widgets
        self.create_input_fields(fields)

        # Create the buttons at the bottom
        self.create_bottom_buttons()

        # Set up the central widget
        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)
        self.setMinimumSize(QSize(400, 600))

    def create_input_fields(self, fields):
        """Creates input fields, labels, and checkboxes for each field."""
        for field in fields:
            label = QLabel(field)
            label.setMinimumWidth(150)

            input_field = QLineEdit()
            input_field.setMinimumSize(QSize(200, 50))
            self.input_fields.append(input_field)

            checkbox = QCheckBox()  # Create a checkbox for selection
            self.checkboxes.append(checkbox)

            row_layout = QHBoxLayout()
            row_layout.addWidget(label)
            row_layout.addWidget(input_field)
            row_layout.addWidget(checkbox)  # Add the checkbox to the layout

            self.main_layout.addLayout(row_layout)

    def create_bottom_buttons(self):
        """Creates the bottom action buttons."""
        bottom_row_layout = QHBoxLayout()
        # Button for importing entries from a CSV file
        self.import_button = QPushButton("Import from CSV")
        self.import_button.setMaximumSize(QSize(200, 50))
        self.import_button.clicked.connect(self.import_entries_from_csv)  # Connect to import function
        bottom_row_layout.addWidget(self.import_button)

        # Button for adding a new entry
        self.add_button = QPushButton("Add Entry")
        self.add_button.setMaximumSize(QSize(200, 50))
        self.add_button.clicked.connect(self.submit_new_entry) # connect to adding function
        bottom_row_layout.addWidget(self.add_button)

        # Button for modifying an existing entry
        self.modify_button = QPushButton("Modify Entry")
        self.modify_button.setMaximumSize(QSize(200, 50))
        self.modify_button.clicked.connect(self.modify_existing_entry) # connect to modify function
        bottom_row_layout.addWidget(self.modify_button)

        # Button for viewing saved entries
        self.view_button = QPushButton("View Entries")
        self.view_button.setMaximumSize(QSize(200, 50))
        self.view_button.clicked.connect(self.view_saved_entries)  # Connect to view function
        bottom_row_layout.addWidget(self.view_button)

        # Button for removing selected entries
        self.remove_selected_button = QPushButton("Remove Selected")
        self.remove_selected_button.setMaximumSize(QSize(200, 50))
        self.remove_selected_button.clicked.connect(self.remove_selected_entries)  # connect to remove function
        bottom_row_layout.addWidget(self.remove_selected_button)

        # Button for exporting entries to a CSV file
        self.export_button = QPushButton("Export to CSV")
        self.export_button.setMaximumSize(QSize(200, 50))
        self.export_button.clicked.connect(self.export_entries_to_csv)  # Connect to export function
        bottom_row_layout.addWidget(self.export_button)

        self.main_layout.addLayout(bottom_row_layout)

    def submit_new_entry(self):
        """Submit the input from all fields and store them as a new entry."""
        firmenname = self.input_fields[0].text().strip()  # Get the Firmenname from the second input field

        if not firmenname:
            QMessageBox.warning(self, "Error", "Firmenname cannot be empty.")
            return

        # Check if the Firmenname already exists
        if firmenname in self.all_entries:
           QMessageBox.warning(self, "Error", "Firmenname already exists.")
           return

        new_entry = {f"Field {i + 1}": input_field.text() for i, input_field in enumerate(self.input_fields)}
        self.all_entries[firmenname] = new_entry  # Store the new entry with Firmenname as the key
        print("Stored Entry:", new_entry)  # Print the entry to console

        # Clear input fields after submission for new entry input
        self.clear_input_fields()

    def modify_existing_entry(self):
        """Modify the currently selected entry."""
        if self.current_entry_key is not None:
            updated_entry = {f"Field {i + 1}": input_field.text() for i, input_field in enumerate(self.input_fields)}
            self.all_entries[self.current_entry_key] = updated_entry  # Update the existing entry
            print("Updated Entry:", updated_entry)
            self.clear_input_fields()
            self.current_entry_key = None  # Reset current key after modification
        else:
            QMessageBox.warning(self, "Error", "No entry selected for modification.")

    def clear_input_fields(self):
        """Clear input fields after submission or modification."""
        for input_field in self.input_fields:
            input_field.clear()
        
        # Reset checkboxes
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

    def remove_selected_entries(self):
        """Clear the input fields corresponding to the checked checkboxes."""
        selected_indices = [i for i in range(len(self.checkboxes)) if self.checkboxes[i].isChecked()]

        # Clear input fields corresponding to the selected checkboxes
        for i in selected_indices:
            if i < len(self.input_fields):
                self.input_fields[i].clear()  # Clear the input field

        # Reset checkboxes after clearing
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

    def view_saved_entries(self):
        """Show a dialog to select and view saved entries."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Entry to View")
        layout = QVBoxLayout()
        list_widget = QListWidget()

        # Populate the list widget with entry names
        for firmenname, entry in self.all_entries.items():
            list_widget.addItem(f"{firmenname}: {entry}")

        list_widget.itemDoubleClicked.connect(lambda item: self.populate_fields(item.text(), dialog))

        layout.addWidget(list_widget)
        dialog.setLayout(layout)
        dialog.exec()  # Show dialog and wait for user interaction

    def populate_fields(self, entry_text, dialog):
        """Populate the input fields with the selected entry from the list."""
        firmenname = entry_text.split(":")[0].strip()  # Extract Firmenname from the text
        if firmenname in self.all_entries:
            entry = self.all_entries[firmenname]

            # Populate the input fields with the selected entry
            for i, input_field in enumerate(self.input_fields):
                input_field.setText(entry[f"Field {i + 1}"])
                
            # Set the current entry key to allow modification
            self.current_entry_key = firmenname
        else:
            QMessageBox.warning(self, "Error", "Could not populate fields.")
        dialog.close()  # Close the dialog after selection
    def import_entries_from_csv(self):
     """Import entries from a CSV file and populate the entries in the app."""
     file_dialog = QFileDialog()
     file_name, _ = file_dialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")

     if not file_name:
        return  # If no file is selected, exit the function

     try:
        with open(file_name, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)

            # Read header
            header = next(reader)
            if header[0] != "Firmenname":
                QMessageBox.warning(self, "Error", "Invalid CSV format. First column must be 'Firmenname'.")
                return

            self.all_entries.clear()  # Clear existing entries before importing

            # Read and import each row
            for row in reader:
                if len(row) < len(self.input_fields) + 1:
                    QMessageBox.warning(self, "Error", "CSV format does not match expected number of fields.")
                    return

                firmenname = row[0].strip()
                if not firmenname:
                    continue  # Skip rows with empty Firmenname

                # Create an entry dictionary based on the fields
                entry = {f"Field {i + 1}": row[i + 1] for i in range(len(self.input_fields))}
                self.all_entries[firmenname] = entry

            # Optionally, populate the input fields with the first entry to give feedback
            first_firmenname = list(self.all_entries.keys())[0]
            first_entry = self.all_entries[first_firmenname]

            for i, input_field in enumerate(self.input_fields):
                input_field.setText(first_entry[f"Field {i + 1}"])

            QMessageBox.information(self, "Success", f"Entries successfully imported from {file_name}.")

     except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to import entries: {str(e)}")

    def export_entries_to_csv(self):
        """Export all saved entries to a CSV-compatible text file."""
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")

        
        if file_name:
            try:
                with open(file_name, mode='w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)

                    # Write header
                    header = ["Firmenname"] + [f"Field {i + 1}" for i in range(len(self.input_fields))]
                    writer.writerow(header)

                    # Write each entry
                    for firmenname, entry in self.all_entries.items():
                        row = [firmenname] + [entry[f"Field {i + 1}"] for i in range(len(self.input_fields))]
                        writer.writerow(row)

                QMessageBox.information(self, "Success", "Entries successfully exported to CSV.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export entries: {str(e)}")

# Create the application instance
app = QApplication([])

# Create the main window
window = MainWindow()
window.show()

# Start the application event loop
sys.exit(app.exec())

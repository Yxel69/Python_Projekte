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
        self.all_entries = {}  # Store all saved entries with Handelsregister as key
        self.current_entry_key = None  # Track the currently selected entry key

        self.fields = [
            "Firmenname",
            "Handelsregister",  # This will be used as the key
            "Straßenname",
            "Hausnummer",
            "PLZ",
            "Ort",
            "Anrede",
            "AP_Vorname",
            "AP_Nachname"
        ]

        # Create input fields and associated widgets
        self.create_input_fields(self.fields)

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

        self.import_button = QPushButton("Import from CSV")
        self.import_button.setMaximumSize(QSize(200, 50))
        self.import_button.clicked.connect(self.import_entries_from_csv)
        bottom_row_layout.addWidget(self.import_button)

        self.add_button = QPushButton("Add Entry")
        self.add_button.setMaximumSize(QSize(200, 50))
        self.add_button.clicked.connect(self.submit_new_entry)
        bottom_row_layout.addWidget(self.add_button)

        self.modify_button = QPushButton("Modify Entry")
        self.modify_button.setMaximumSize(QSize(200, 50))
        self.modify_button.clicked.connect(self.modify_existing_entry)
        bottom_row_layout.addWidget(self.modify_button)

        self.view_button = QPushButton("View Entries")
        self.view_button.setMaximumSize(QSize(200, 50))
        self.view_button.clicked.connect(self.view_saved_entries)
        bottom_row_layout.addWidget(self.view_button)

        self.remove_selected_button = QPushButton("Remove Selected")
        self.remove_selected_button.setMaximumSize(QSize(200, 50))
        self.remove_selected_button.clicked.connect(self.remove_selected_entries)
        bottom_row_layout.addWidget(self.remove_selected_button)

        self.export_button = QPushButton("Export to CSV")
        self.export_button.setMaximumSize(QSize(200, 50))
        self.export_button.clicked.connect(self.export_entries_to_csv)
        bottom_row_layout.addWidget(self.export_button)

        self.main_layout.addLayout(bottom_row_layout)

    def submit_new_entry(self):
        """Submit the input from all fields and store them as a new entry."""
        handelsregister = self.input_fields[1].text().strip()  # Get the Handelsregister (new primary key)

        if not handelsregister:
            QMessageBox.warning(self, "Error", "Handelsregister cannot be empty.")
            return

        # Check if the Handelsregister already exists
        if handelsregister in self.all_entries:
            QMessageBox.warning(self, "Error", "Handelsregister already exists.")
            return

        new_entry = {f"Field {i + 1}": input_field.text() for i, input_field in enumerate(self.input_fields)}
        self.all_entries[handelsregister] = new_entry  # Store the new entry with Handelsregister as the key
        print("Stored Entry:", new_entry)

        # Clear input fields after submission for new entry input
        self.clear_input_fields()

    def modify_existing_entry(self):
        """Modify the currently selected entry."""
        if self.current_entry_key is not None:
            updated_entry = {f"Field {i + 1}": input_field.text() for i, input_field in enumerate(self.input_fields)}
            self.all_entries[self.current_entry_key] = updated_entry  # Update the existing entry
            print("Updated Entry:", updated_entry)
            self.clear_input_fields()
            self.current_entry_key = None  # Reset current entry after modification
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
        for handelsregister, entry in self.all_entries.items():
            list_widget.addItem(f"{handelsregister}: {entry}")

        list_widget.itemDoubleClicked.connect(lambda item: self.populate_fields(item.text(), dialog))

        layout.addWidget(list_widget)
        dialog.setLayout(layout)
        dialog.exec()

    def populate_fields(self, entry_text, dialog):
        """Populate the input fields with the selected entry from the list."""
        handelsregister = entry_text.split(":")[0].strip()  # Extract Handelsregister from the text
        if handelsregister in self.all_entries:
            entry = self.all_entries[handelsregister]

            # Populate the input fields with the selected entry
            for i, input_field in enumerate(self.input_fields):
                input_field.setText(entry[f"Field {i + 1}"])

            # Set the current entry key to allow modification
            self.current_entry_key = handelsregister
        else:
            QMessageBox.warning(self, "Error", "Could not populate fields.")
        dialog.close()

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
                if header[1] != "Handelsregister":  # Handelsregister should be the second field
                    QMessageBox.warning(self, "Error", "Invalid CSV format. Second column must be 'Handelsregister'.")
                    return

                self.all_entries.clear()  # Clear existing entries before importing

                # Read and import each row
                for row in reader:
                    if len(row) < len(self.input_fields):
                        QMessageBox.warning(self, "Error", "CSV format does not match expected number of fields.")
                        return

                    handelsregister = row[1].strip()  # Handelsregister is now the primary key
                    if not handelsregister:
                        continue  # Skip rows without Handelsregister

                    entry = {f"Field {i + 1}": row[i] for i in range(len(self.input_fields))}
                    self.all_entries[handelsregister] = entry

                QMessageBox.information(self, "Success", "Entries imported successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to import entries: {e}")

    def export_entries_to_csv(self):
        """Export all entries to a CSV file."""
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")

        if not file_name:
            return  # If no file is selected, exit the function

        try:
            with open(file_name, mode='w', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write header
                writer.writerow(self.fields)

                # Write each entry
                for handelsregister, entry in self.all_entries.items():
                    row = [entry[f"Field {i + 1}"] for i in range(len(self.input_fields))]
                    writer.writerow(row)

                QMessageBox.information(self, "Success", "Entries exported successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to export entries: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

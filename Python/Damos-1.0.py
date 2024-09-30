import sys
import os
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
)

from PyQt6.QtGui import QIcon

os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Damos-Datenbankeingabe")
        self.setWindowIcon(QIcon("pikachu.png"))
        self.main_layout = QVBoxLayout()

        # Initialize input fields and entry storage
        self.input_fields = []
        self.checkboxes = []  # To store checkboxes for selection
        self.all_entries = {}  # Store all saved entries with Firmenname as key
        self.current_entry_key = None  # Track the currently selected entry key

        fields = [
            "Handelsregisternummer:",
            "Firmenname:",  # This will be used as the key
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
            label.setMinimumWidth(135)

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

        # Button for adding a new entry
        self.add_button = QPushButton("Add Entry")
        self.add_button.setMaximumSize(QSize(200, 50))
        self.add_button.clicked.connect(self.submit_new_entry)
        bottom_row_layout.addWidget(self.add_button)

        # Button for modifying an existing entry
        self.modify_button = QPushButton("Modify Entry")
        self.modify_button.setMaximumSize(QSize(200, 50))
        self.modify_button.clicked.connect(self.modify_existing_entry)
        bottom_row_layout.addWidget(self.modify_button)

        # Button for viewing saved entries
        self.view_button = QPushButton("View Entries")
        self.view_button.setMaximumSize(QSize(200, 50))
        self.view_button.clicked.connect(self.view_saved_entries)  # Connect to view function
        bottom_row_layout.addWidget(self.view_button)

        # Button for removing selected entries
        self.remove_selected_button = QPushButton("Remove Selected")
        self.remove_selected_button.setMaximumSize(QSize(200, 50))
        self.remove_selected_button.clicked.connect(self.remove_selected_entries)  # Connect to remove function
        bottom_row_layout.addWidget(self.remove_selected_button)

        self.main_layout.addLayout(bottom_row_layout)

    def submit_new_entry(self):
        """Submit the input from all fields and store them as a new entry."""
        firmenname = self.input_fields[1].text().strip()  # Get the Firmenname from the second input field

        if not firmenname:
            QMessageBox.warning(self, "Error", "Firmenname cannot be empty.")
            return

        # Check if the Firmenname already exists
        if firmenname in self.all_entries:
            overwrite = QMessageBox.question(
                self, "Overwrite Entry", f"Entry with Firmenname '{firmenname}' already exists. Overwrite?",
                QMessageBox.Yes | QMessageBox.No
            )
            if overwrite == QMessageBox.No:
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

# Create the application instance
app = QApplication([])

# Create the main window
window = MainWindow()
window.show()

# Start the application event loop
sys.exit(app.exec())

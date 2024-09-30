import sys
import os
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow,QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtGui import QIcon
os.system('cls' if os.name =='nt' else 'clear')         #clear terminal window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        entrys = []
        self.setWindowTitle("Damos")
        self.setWindowIcon(QIcon("pikachu.png"))

        # Create the main vertical layout to hold all rows
        self.main_layout = QVBoxLayout()

        # List to store the input fields and buttons
        self.input_fields = []
        self.edit_buttons = []
        self.stored_company_codes = []
        '''
        Auswahl mehrerer Modi : einsehen, einfügen, bearbeiten, löschen
        '''
        # Number of rows needed
        needed_fields = 9
        fields=["Handelsregisternummer:","Firmenname:","Straßenname:","Hausnummer:","PLZ:","Ort:","Anrede:","AP_Vorname:","AP_Nachname:"]
        
        # Create multiple rows of label, input field, and edit button
        for i in range(needed_fields):
            # Label for each field
            label = QLabel(fields[i])
            label.setMinimumWidth(135)
            # Input field for each company code
            self.input_field = QLineEdit()
            self.input_field.setEchoMode(QLineEdit.EchoMode.Normal)
            self.input_field.setFrame(True)
            self.input_field.setMinimumSize(QSize(200, 50))
            
            self.input_fields.append(self.input_field)  # Add the input field to the list
            
            # Create an edit button for each row
            edit_button = QPushButton("Edit")
            edit_button.setMaximumSize(QSize(100, 50))
            edit_button.setEnabled(False)  # Initially disable the edit button
            edit_button.clicked.connect(lambda checked, i=i: self.edit_entry(i))  # Connect to edit function
            self.edit_buttons.append(edit_button)  # Add the edit button to the list

            # Create a horizontal layout for the label, input field, and edit button
            row_layout = QHBoxLayout()
            row_layout.addWidget(label)
            row_layout.addWidget(self.input_field)
            row_layout.addWidget(edit_button)

            # Add this horizontal layout to the main vertical layout
            self.main_layout.addLayout(row_layout)

       # Create a single button at the bottom
        bottom_row_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit Entry")
        self.submit_button.setMaximumSize(QSize(200, 50))
        self.submit_button.clicked.connect(self.submit_all_inputs)
        bottom_row_layout.addWidget(self.submit_button)
        # Add the button to the main layout
        self.main_layout.addLayout(bottom_row_layout)

        # Create a central widget and set the main vertical layout
        widget = QWidget()
        widget.setLayout(self.main_layout)

        # Set the central widget for the window
        self.setCentralWidget(widget)

        # Set the minimum window size
        self.setMinimumSize(QSize(400, 600))

    # Button click handler to submit all inputs
    def submit_all_inputs(self):
        # Clear the list before storing new data
        self.stored_company_codes = []

        # Collect the text from all input fields and store them in the list
        for input_field in self.input_fields:
            codes = input_field.text()
            self.stored_company_codes.append(codes)

        # Print the list of company codes
        print("Stored Company Codes:", self.stored_company_codes)

        # Enable all the edit buttons
        for button in self.edit_buttons:
            button.setEnabled(True)

    # Edit button click handler for a specific row
    def edit_entry(self, index):
        # Get the corresponding input field and enable it for editing
        input_field = self.input_fields[index]
        input_field.setReadOnly(False)  # Allow editing
        
        # Print out which entry is being edited
        print(f"Editing Company Code {index+1}: {self.stored_company_codes[index]}")

        # Update stored value when editing is finished
        def update_value():
            # Get the updated value
            new_value = self.input_field.text()
            self.stored_company_codes[index] = new_value  # Update the stored value
            print(f"Updated Company Code {index+1}: {new_value}")

        # Connect the update action to the input field's editingFinished signal
        input_field.editingFinished.connect(update_value)

# Create the application instance
app = QApplication([])

# Create the main window
window = MainWindow()
window.show()

# Start the application event loop
sys.exit(app.exec())

import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import os
import hashlib
import string

class Student:
    id_counter = 0

    def __init__(self, name, birthday, course, address, email):
        Student.id_counter += 1
        self.id = f"TUP-M-{Student.id_counter:04d}"
        self.name = name
        self.birthday = birthday
        self.age = self.calculate_age(birthday)
        self.course = course
        self.address = address
        self.email = email

    def calculate_age(self, birthday):
        today = datetime.date.today()
        birth_date = datetime.datetime.strptime(birthday, "%Y-%m-%d").date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

class StudentSystem:
    def __init__(self):
        self.students = []
        self.load_data()

    def load_data(self):
        if os.path.exists('students.txt'):
            with open('students.txt', 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    student = Student(data[1], data[2], data[3], data[4], data[5])
                    student.id = data[0]
                    self.students.append(student)
            Student.id_counter = int(data[0].split('-')[-1]) 

    def save_data(self):
        with open('students.txt', 'w') as file:
            for student in self.students:
                file.write(f"{student.id},{student.name},{student.birthday},{student.course},{student.address},{student.email}\n")

    def add_student(self, student):
        self.students.append(student)
        self.save_data()

    def update_student(self, index, student):
        self.students[index] = student
        self.save_data()

    def delete_student(self, index):
        del self.students[index]
        self.save_data()

class SubstitutionCipher:
    @staticmethod
    def encrypt(text, key):
        alphabet = string.ascii_lowercase
        encrypted_text = ""
        for char in text.lower():
            if char in alphabet:
                encrypted_text += key[alphabet.index(char)]
            else:
                encrypted_text += char
        return encrypted_text

    @staticmethod
    def decrypt(encrypted_text, key):
        alphabet = string.ascii_lowercase
        decrypted_text = ""
        for char in encrypted_text:
            if char in key:
                decrypted_text += alphabet[key.index(char)]
            else:
                decrypted_text += char
        return decrypted_text

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Information System")
        self.geometry("400x300")
        self.system = StudentSystem()
        self.configure(bg="black")  # Setting background color to black

        self.menu_label = tk.Label(self, text="Main Menu", font=("Helvetica", 16), bg="black", fg="white")  # Changing label background to black and text color to white
        self.menu_label.pack(pady=10)

        self.encrypt_button = tk.Button(self, text="Encrypt a Record", command=self.encrypt_menu, bg="black", fg="white")  # Changing button background to black and text color to white
        self.encrypt_button.pack(pady=5)

        self.decrypt_button = tk.Button(self, text="Decrypt a Record", command=self.decrypt_menu, bg="black", fg="white")  # Changing button background to black and text color to white
        self.decrypt_button.pack(pady=5)

        self.made_by_label = tk.Label(self, text="Made by Ryan", bg="black", fg="white")  # Changing label background to black and text color to white
        self.made_by_label.pack(pady=5)

    def encrypt_menu(self):
        ytpassword = "yasuo"
        entered_password = simpledialog.askstring("Enter Password", "Please enter the password to continue:")

        if entered_password != ytpassword:
            messagebox.showerror("Error", "Incorrect password.")
            return
        
        encrypt_menu = tk.Toplevel(self)
        encrypt_menu.title("Encrypt Menu")
        encrypt_menu.geometry("300x200")
        encrypt_menu.configure(bg="black")  # Setting background color to black

        add_button = tk.Button(encrypt_menu, text="Add Student", command=self.add_student, bg="black", fg="white")  # Changing button background to black and text color to white
        add_button.pack(pady=5)

        view_button = tk.Button(encrypt_menu, text="View Students", command=self.view_students, bg="black", fg="white")  # Changing button background to black and text color to white
        view_button.pack(pady=5)

        update_button = tk.Button(encrypt_menu, text="Update Student", command=self.update_student, bg="black", fg="white")  # Changing button background to black and text color to white
        update_button.pack(pady=5)

        delete_button = tk.Button(encrypt_menu, text="Delete Student", command=self.delete_student, bg="black", fg="white")  # Changing button background to black and text color to white
        delete_button.pack(pady=5)

        encrypt_button = tk.Button(encrypt_menu, text="Encrypt Student Data", command=self.encrypt_student_data, bg="black", fg="white")  # Changing button background to black and text color to white
        encrypt_button.pack(pady=5)

    def add_student(self):
        name = simpledialog.askstring("Add Student", "Enter Name:")
        birthday = simpledialog.askstring("Add Student", "Enter Birthday (YYYY-MM-DD):")
        course = simpledialog.askstring("Add Student", "Enter Course:")
        address = simpledialog.askstring("Add Student", "Enter Address:")
        email = simpledialog.askstring("Add Student", "Enter Email Address:")

        student = Student(name, birthday, course, address, email)
        self.system.add_student(student)

    def view_students(self):
        if self.system.students:
            student_info = "\n".join([f"ID: {student.id}, Name: {student.name}, Birthday: {student.birthday}, Age: {student.age}, Course: {student.course}, Address: {student.address}, Email: {student.email}" for student in self.system.students])
            messagebox.showinfo("View Students", student_info)
        else:
            messagebox.showinfo("View Students", "No students added yet.")

    def update_student(self):
        if not self.system.students:
            messagebox.showinfo("Update Student", "No students added yet.")
            return

        student_id = simpledialog.askstring("Update Student", "Enter ID of Student to Update:")
        for index, student in enumerate(self.system.students):
            if student.id == student_id:
                name = simpledialog.askstring("Update Student", "Enter Name:")
                birthday = simpledialog.askstring("Update Student", "Enter Birthday (YYYY-MM-DD):")
                course = simpledialog.askstring("Update Student", "Enter Course:")
                address = simpledialog.askstring("Update Student", "Enter Address:")
                email = simpledialog.askstring("Update Student", "Enter Email Address:")

                student.name = name
                student.birthday = birthday
                student.age = student.calculate_age(birthday)
                student.course = course
                student.address = address
                student.email = email

                self.system.update_student(index, student)
                break
        else:
            messagebox.showinfo("Update Student", f"No student found with ID: {student_id}")

    def delete_student(self):
        if not self.system.students:
            messagebox.showinfo("Delete Student", "No students added yet.")
            return

        student_id = simpledialog.askstring("Delete Student", "Enter ID of Student to Delete:")
        for index, student in enumerate(self.system.students):
            if student.id == student_id:
                confirmation = messagebox.askyesno("Delete Student", f"Are you sure you want to delete {student.name}?")
                if confirmation:
                    self.system.delete_student(index)
                break
        else:
            messagebox.showinfo("Delete Student", f"No student found with ID: {student_id}")

    def encrypt_student_data(self):
        if not self.system.students:
            messagebox.showinfo("Encrypt Data", "No students added yet.")
            return

        password = simpledialog.askstring("Set Password", "Set Encryption Password:")
        if not password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        encrypted_students = []
        for student in self.system.students:
            encrypted_data = self.encrypt_data(student, hashed_password)
            encrypted_students.append(encrypted_data)

        with open("studentrec.txt", "w") as file:
            for encrypted_student in encrypted_students:
                file.write(encrypted_student + "\n")
        messagebox.showinfo("Encrypt Data", "Student data encrypted and saved as studentrec.txt")

    def encrypt_data(self, student, password_hash):
        encrypted_id = SubstitutionCipher.encrypt(student.id, self.key)
        encrypted_name = SubstitutionCipher.encrypt(student.name, self.key)
        encrypted_birthday = SubstitutionCipher.encrypt(student.birthday, self.key)
        encrypted_course = SubstitutionCipher.encrypt(student.course, self.key)
        encrypted_address = SubstitutionCipher.encrypt(student.address, self.key)
        encrypted_email = SubstitutionCipher.encrypt(student.email, self.key)
        encrypted_data = f"{encrypted_id},{encrypted_name},{encrypted_birthday},{encrypted_course},{encrypted_address},{encrypted_email},{password_hash}"
        return encrypted_data

    def decrypt_menu(self):
        decrypt_menu = tk.Toplevel(self)
        decrypt_menu.title("Decrypt Menu")
        decrypt_menu.geometry("300x150")
        decrypt_menu.configure(bg="black")  # Setting background color to black

        file_label = tk.Label(decrypt_menu, text="Enter the TXT file:", bg="black", fg="white")  # Changing label background to black and text color to white
        file_label.pack(pady=5)

        self.file_entry = tk.Entry(decrypt_menu, bg="black", fg="white")  # Changing entry background to black and text color to white
        self.file_entry.pack(pady=5)

        password_label = tk.Label(decrypt_menu, text="Enter the Password:", bg="black", fg="white")  # Changing label background to black and text color to white
        password_label.pack(pady=5)

        self.password_entry = tk.Entry(decrypt_menu, show="*", bg="black", fg="white")  # Changing entry background to black and text color to white
        self.password_entry.pack(pady=5)

        decrypt_button = tk.Button(decrypt_menu, text="Decrypt", command=self.decrypt_student_data, bg="black", fg="white")  # Changing button background to black and text color to white
        decrypt_button.pack(pady=5)

    def decrypt_student_data(self):
        file_name = self.file_entry.get()
        password = self.password_entry.get()

        if not os.path.exists(file_name):
            messagebox.showerror("Error", "File not found.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        decrypted_students = []
        with open(file_name, "r") as file:
            for line in file:
                decrypted_student = self.decrypt_data(line.strip(), hashed_password)
                if decrypted_student:
                    decrypted_students.append(decrypted_student)

        if decrypted_students:
            messagebox.showinfo("Decrypted Student Data", "\n".join(decrypted_students))
        else:
            messagebox.showerror("Decryption Failed", "Incorrect password or no valid records found.")

    def decrypt_data(self, encrypted_data, password_hash):
        encrypted_fields = encrypted_data.split(',')
        if len(encrypted_fields) != 7:  
            return None

        encrypted_password_hash = encrypted_fields[-1].strip()  
        if encrypted_password_hash != password_hash: 
            return None

        decrypted_data = ""
        decrypted_id = SubstitutionCipher.decrypt(encrypted_fields[0], self.key)
        decrypted_name = SubstitutionCipher.decrypt(encrypted_fields[1], self.key)
        decrypted_birthday = SubstitutionCipher.decrypt(encrypted_fields[2], self.key)
        decrypted_course = SubstitutionCipher.decrypt(encrypted_fields[3], self.key)
        decrypted_address = SubstitutionCipher.decrypt(encrypted_fields[4], self.key)
        decrypted_email = SubstitutionCipher.decrypt(encrypted_fields[5], self.key)
        decrypted_data = f"ID: {decrypted_id}, Name: {decrypted_name}, Birthday: {decrypted_birthday}, Course: {decrypted_course}, Address: {decrypted_address}, Email: {decrypted_email}"
        return decrypted_data

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
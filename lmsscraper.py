# This code was written by Nagi Nagiyev in 08.27.2023
# The code is created for just as a help to my friends and make their works easier.
# Have fun! :)

import time
import datetime
import tkinter as tk
from tkinter import ttk
import keyboard
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import threading

# List to keep labels(labels called _subject_name_label and info) of previous iteration to delete some labels for second iteration
labels = []

# Enter button function
def enter_function():

    # For loop to destroy labels(labels called _subject_name_label and info) of previous iteration
    for label in labels:
        label.destroy()
    
    # Clean error message for next iteration
    error_happened_label.config(text="")
    note_label.config(text="")

    # Clean Loading message for the next iteration
    loading_percent.config(text="")

    # Label for a message which shows "Please wait..."
    loading_percent.config(text="Please wait...")
    loading_percent.place(x=75, y=240)

    # Get username, password, browser and semester
    username = username_entry.get()
    password = password_entry.get()
    semester = selected_semester.get()
    selected_index = years_menu.current()
    selected_year_index = selected_index + 1

    # Checks which browser you choosed and do process according this browser
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    robot = webdriver.Chrome(options=chrome_options)

    # Minimize cmd 
    keyboard.press_and_release("win+down")

    # Link of the website for scraping 
    link = "http://lms.adnsu.az/adnsuEducation/login.jsp"
    robot.get(link)
    wait = WebDriverWait(robot, 10)

    try:

        # This code find username and password fields to write user's username and password then click enter for logging in account
        username_field = wait.until(EC.visibility_of_element_located((By.ID, "username")))
        username_field.send_keys(username)
        password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password_field.send_keys(password + Keys.ENTER)

        # Finds "Sistemlər" and click it 
        sistemler = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div/div[1]/ul/li/a/span')))
        sistemler.click()

        # Finds "Tədris prosesi" and click it 
        tedris_prosesi = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div/div[1]/ul/li/ul/div/div[2]/a/small')))
        tedris_prosesi.click()

        # Finds "Fənn üzrə qruplar" and click it
        fenn_uzre_qruplar = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'Fənn üzrə qruplar')))
        fenn_uzre_qruplar.click()

        # Click an empty place in the window to close pop-up
        script = "document.getElementById('accordionDiv').click();"
        robot.execute_script(script)

        # Click dropdown button and select year 
        dropdown_year = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@data-id="subject_edu_year"]')))
        dropdown_year.click()
        year = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="operationDiv"]/div[2]/div/div/div/div[1]/div/div/ul/li[{selected_year_index}]/a')))
        year.click()

        # Click dropdown button and select semester according your choice
        dropdown_semester = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@data-id="subject_semester"]')))
        dropdown_semester.click()
        if semester == "Spring":
            semester = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="operationDiv"]/div[2]/div/div/div/div[2]/div/div/ul/li[2]')))
            semester.click()
        elif semester == "Autumn":
            semester = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="operationDiv"]/div[2]/div/div/div/div[2]/div/div/ul/li[1]')))
            semester.click()
        
        # Finds how many subjects are there and create a for loop for each subject
        number_of_subjects = len(wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'state-link'))))
        # increase show how processing percentage will change for every iteration
        increase = int(100 / number_of_subjects)
        # percentage is for to start process from zero percentage
        percentage = 0

        # Change the text of "Please wait..." into "Processing 0%"
        loading_percent.config(text="Processing 0%")
        # The starting position of label called info (important to show data starting from left to right like in program)
        x_position = 14
        y_position = 350

        # For loop to print data of each subject 
        for i in range(0, number_of_subjects):

            # Finds subject by its index and click it 
            subject = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'state-link')))[i]
            subject.click()

            # Finds subject's name to show it in the application as a label
            subject_name = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/h1')))

            # Update the root to show "Processing 0%", increase percentage, and change the "Processing 0%" to new percentage       
            root.update()
            percentage = percentage + increase
            loading_percent.config(text=f"Processing {percentage}%")

            # Finds "Elektron jurnal" and click it. Finds "Yekun jurnal" and click it. Finds "Göstər" and click it. To get table 
            # where our data is located
            elektron_jurnal = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'Elektron jurnal')))
            elektron_jurnal.click()
            yekun_jurnal = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'Yekun jurnal')))
            yekun_jurnal.click() 
            goster = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'Göstər')))
            goster.click()

            # Finds all keys in the table
            keys_table = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="resultJournal"]/thead/tr')))
            keys = keys_table.find_elements(By.TAG_NAME, 'th')

            # Finds all values in the table
            values_table = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="resultJournal"]/tbody')))
            values = values_table.find_elements(By.TAG_NAME, 'td')

            # Create a label for subject name and add subject name label to our list called labels. Becaues if there will
            # be a second iteration, we should delete first iteration's label to avoid overwrite new label into previous.    
            subject_name_label = tk.Label(root, text=(subject_name.text)[:23], bg="#303030", fg="white", font=header_font)
            subject_name_label.place(x=x_position, y=300)
            labels.append(subject_name_label)

            # 1. Print all key and value pairs
            # 2. Add label called info to labels list 
            # 3. Change the position of next label for a look from left to right as in program
            for key, value in zip(keys[2:], values[2:]):
                info = tk.Label(root, text=f"{key.text} : {value.text}", bg="#303030", fg="white", font=text_font)
                info.place(x=x_position, y=y_position)
                labels.append(info)
                y_position += 25
            y_position = 350
            x_position += 210

            # Make program go back where all subjects are located
            fennler_siyahisi = wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'Fənnlər siyahısı')))
            fennler_siyahisi.click()

            # Ends percentage to "Done!" message
            if percentage > 95:
                loading_percent.config(text=f"Processing 100%")
                root.update()
                time.sleep(1)
                robot.quit()
                loading_percent.config(text="Done!")
                root.update()
        x_position += 210

    # Shows an exception label when there is an error
    except TimeoutException:
        loading_percent.config(text="")
        error_happened_label.config(text="Error happened. Please try again")
        note_label.config(text="NOTE : Error reason can be according to wrong username or password, slow internet or web-page based problem")
        error_happened_label.place(x=10, y=280)
        note_label.place(x=10, y=310)
        robot.quit()
        root.update()

# Thread for doing all scraping process in the background. If there is not a thread, program cannot respond in some cases 
def enter_starter():
    process = threading.Thread(target=enter_function)
    process.start()

# ---CREATING GUI FOR THE PROJECT---

# Root configurations and some styles 
root = tk.Tk()
root.state('zoomed')
root.title("Scrippy")
root.configure(bg="#303030")
header_font = ("Arial", 11, "bold")
text_font = ("Bahnschrift", 11)
radio_button_style = {"bg": "#303030", "fg": "black", "font": text_font}

# Username Entry
username_label = tk.Label(root, text="Username", bg="#303030", fg="white", font=header_font)
username_label.pack(pady=3, padx=10, anchor='w')
username_entry = tk.Entry(root, font=text_font, width=20)
username_entry.pack(pady=5, padx=10, anchor='w')

# Separator or Empty Space
separator = tk.Frame(root, height=15, bg="#303030")
separator.pack()

# Password Entry
password_label = tk.Label(root, text="Password", bg="#303030", fg="white", font=header_font)
password_label.pack(pady=3, padx=10, anchor='w')
password_entry = tk.Entry(root, show="x", font=text_font, width=20)
password_entry.pack(pady=5, padx=10, anchor='w')

# Enter Button
enter_button = tk.Button(root, text="Enter", command=enter_starter, font=header_font, height=1, width=10)
enter_button.pack(pady=10, padx=42, anchor='w')
enter_button.config(bg="green")

# Drawing a long line
string = "_" * 170
line = tk.Label(root, text=string, bg="#303030", fg="white", font=header_font)
line.pack(pady=10, padx=10, anchor='w')

# Data label
data_text = tk.Label(root, text="Data",  bg="#303030", fg="white", font=header_font)
data_text.pack(pady=5, padx=10, anchor='w')

# Semester radio buttons
semester_text = tk.Label(root, text="Semester", bg="#303030", fg="white", font=header_font)
semester_text.place(x=275, y=3)

selected_semester = tk.StringVar()
selected_semester.set("Autumn")

autumn = tk.Radiobutton(root, text="Autumn", variable=selected_semester, value="Autumn", **radio_button_style)
spring = tk.Radiobutton(root, text="Spring", variable=selected_semester, value="Spring", **radio_button_style)

autumn.place(x=275, y=40)
spring.place(x=275, y=70)

# Choose Year
current_year = datetime.datetime.now().year
years = [f"{year}-{year+1}" for year in range(2010, current_year + 1)]

year_text = tk.Label(root, text="Year", bg="#303030", fg="white", font=header_font)
year_text.place(x=400, y=3)

years_menu = ttk.Combobox(root, values=years, state="readonly")
years_menu.place(x=400, y=40)
years_menu.set(years[-1])

# Error label
error_happened_label = tk.Label(root, text="", bg="#303030", fg="red", font=header_font)
note_label = tk.Label(root, text="", bg="#303030", fg="red", font=header_font)
error_happened_label.place(x=10, y=280)
note_label.place(x=10, y=310)

# Loading Label
loading_percent = tk.Label(root, text="",  bg="#303030", fg="white", font=header_font)
loading_percent.place(x=75, y=240)

root.mainloop()

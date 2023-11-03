import random
import smtplib
import ssl
import tkinter as tk
from tkinter import messagebox

otp = random.randint(100000, 999999)
otp_str = str(otp)
previous_email = ""
def send_email(receiver_email, otp):
    sender_email = "Enter Your EMail"
    sender_password = "Enter Your Password"
    message = "Subject: OTP Verification\n\nYour OTP is " + otp
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
        print("OTP sent successfully!")
        server.quit()
        return True
    except Exception as e:
        print("Error occurred: ", e)
        return False
def resend_otp():
    global otp_str
    if previous_email:
        if send_email(previous_email, otp_str):
            messagebox.showinfo("Success", "OTP resent successfully!")
        else:
            messagebox.showerror("Error", "Unable to resend OTP. Please check your email settings.")
    else:
        messagebox.showerror("Error", "No previous email to resend OTP.")
def verify_otp(otp_entry, otp_window):
    user_otp = otp_entry.get()
    if user_otp == otp_str:
        messagebox.showinfo("Success", "OTP Verification is Successful!")
        otp_window.destroy()
        show_final_message()
    else:
        messagebox.showerror("Error", "OTP Verification failed. Please try again.")
def restart_app():
    global otp, otp_str
    otp = random.randint(100000, 999999)
    otp_str = str(otp)
    final_message.destroy()
    email_window.deiconify()
    email_entry.delete(0, 'end')
    otp_entry.delete(0, 'end')
def close_app():
    final_message.destroy()
    email_window.destroy()
def show_final_message():
    global final_message
    final_message = tk.Tk()
    final_message.title("Final Message")
    final_label = tk.Label(final_message, text="What would you like to do next?")
    final_label.pack()
    send_another_button = tk.Button(final_message, text="Send OTP for another email", command=restart_app)
    exit_button = tk.Button(final_message, text="EXIT", command=close_app)
    send_another_button.pack()
    exit_button.pack()
    final_message.mainloop()
def send_email_and_open_otp_window():
    global previous_email
    user_email = email_entry.get()
    previous_email = user_email
    if send_email(user_email, otp_str):
        messagebox.showinfo("Success", "OTP sent successfully!")
        email_window.withdraw()
        otp_window = tk.Tk()
        otp_window.title("Enter OTP")
        otp_label = tk.Label(otp_window, text="Enter the OTP you received:")
        otp_label.pack()
        global otp_entry
        otp_entry = tk.Entry(otp_window)
        otp_entry.pack()
        verify_button = tk.Button(otp_window, text="Verify OTP", command=lambda: verify_otp(otp_entry, otp_window))
        verify_button.pack()
        resend_otp_button = tk.Button(otp_window, text="Resend OTP", command=resend_otp)
        resend_otp_button.pack()
        otp_window.mainloop()
email_window = tk.Tk()
email_window.title("Email Entry")
email_label = tk.Label(email_window, text="Enter your email address:")
email_label.pack()
email_entry = tk.Entry(email_window)
email_entry.pack()
send_button = tk.Button(email_window, text="Send", command=send_email_and_open_otp_window)
send_button.pack()
email_window.mainloop()

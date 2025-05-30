import tkinter as tk
import subprocess

def connection():
    """
    This function adds an iptables rule to drop outgoing TCP traffic on port 2010,
    and then retrieves and displays the current iptables output.
    """
    try:
        # Append rule to drop connection on port 2010
        # List iptables rules to verify
        subprocess.run(["sudo", "iptables", "-D", "OUTPUT", "-p", "tcp", "--dport", "2010", "-j", "DROP"], check=True)
        result = subprocess.run(["sudo", "iptables", "-L", "-v"], capture_output=True, text=True, check=True)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result.stdout)
    except subprocess.CalledProcessError as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error executing command:\n{e}")

def kill_connection_ragian():
    """
    This function deletes the iptables rule that was used to drop outgoing TCP traffic on port 2010.
    """
    try:
        # Delete the rule for port 2010
        subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-p", "tcp", "--dport", "2010", "-j", "DROP"], check=True)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Connection rule deleted successfully.")
    except subprocess.CalledProcessError as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error executing command:\n{e}")

# Create the main window
root = tk.Tk()
root.title("Connection Manager")

# Create a button for applying the connection rule
conn_button = tk.Button(root, text="Connection", command=connection, width=25)
conn_button.pack(pady=10)

# Create a button for removing the connection rule
kill_button = tk.Button(root, text="Kill Connection Ragian", command=kill_connection_ragian, width=25)
kill_button.pack(pady=10)

# A text widget to display output from the commands
output_text = tk.Text(root, height=15, width=60)
output_text.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()

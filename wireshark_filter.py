import tkinter as tk
from tkinter import filedialog, ttk
import pyshark
from pymavlink import mavutil


class PacketFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wireshark Packet Filter")
        
        # Frame for file selection
        frame = tk.Frame(root)
        frame.pack(pady=10)
        
        self.file_label = tk.Label(frame, text="No file selected")
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        file_button = tk.Button(frame, text="Select File", command=self.load_file)
        file_button.pack(side=tk.LEFT, padx=5)
        
        # Frame for filters
        filter_frame = tk.LabelFrame(root, text="Filters")
        filter_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        tk.Label(filter_frame, text="Protocol:").grid(row=0, column=0, padx=5, pady=5)
        self.protocol_entry = tk.Entry(filter_frame)
        self.protocol_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(filter_frame, text="Source IP:").grid(row=1, column=0, padx=5, pady=5)
        self.src_entry = tk.Entry(filter_frame)
        self.src_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(filter_frame, text="Destination IP:").grid(row=2, column=0, padx=5, pady=5)
        self.dst_entry = tk.Entry(filter_frame)
        self.dst_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(filter_frame, text="MAVLink Command:").grid(row=3, column=0, padx=5, pady=5)
        self.msgid_entry = tk.Entry(filter_frame)
        self.msgid_entry.grid(row=3, column=1, padx=5, pady=5)
        
        apply_button = tk.Button(filter_frame, text="Apply Filter", command=self.apply_filter)
        apply_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Frame for results
        result_frame = tk.LabelFrame(root, text="Results")
        result_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(result_frame, columns=("No", "Time", "Source", "Destination", "Protocol", "MAVLink Command"), show="headings")
        self.tree.heading("No", text="No")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Source", text="Source")
        self.tree.heading("Destination", text="Destination")
        self.tree.heading("Protocol", text="Protocol")
        self.tree.heading("MAVLink Command", text="MAVLink Command")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.bind("<<TreeviewSelect>>", self.display_packet_details)
        
        # Frame for packet details
        detail_frame = tk.LabelFrame(root, text="Packet Details")
        detail_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.detail_text = tk.Text(detail_frame, wrap=tk.WORD, height=15)
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        
        self.capture = None
    
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PCAP Files", "*.pcapng *.pcap")])
        if file_path:
            self.file_label.config(text=file_path)
            self.capture = pyshark.FileCapture(file_path)
            
            try:
                # Force loading of packets to ensure they are available
                self.capture.load_packets()
                print(f"Loaded {len(self.capture)} packets")
                self.populate_tree()
            except Exception as e:
                print(f"Error loading packets: {e}")
    
    def get_mavlink_command_name(self, msgid):
        """Get the MAVLink command name using mavutil."""
        try:
            return mavutil.mavlink.MESSAGES.get(msgid, f"Unknown ({msgid})")


        except Exception as e:
            print(f"Error mapping msgid {msgid}: {e}")
            return f"Unknown ({msgid})"
    
    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        if not self.capture:
            return
        
        for i, packet in enumerate(self.capture):
            try:
                if "IP" in packet:
                    src = packet.ip.src
                    dst = packet.ip.dst
                    proto = packet.highest_layer
                    time = packet.sniff_time.strftime("%H:%M:%S.%f")
                    
                    # Extract MsgID from MAVLINK_PROTO layer
                    command_name = "N/A"
                    if "MAVLINK_PROTO" in packet:
                        msgid = packet["MAVLINK_PROTO"].get_field_value("msgid")
                        if msgid:
                            command_name = self.get_mavlink_command_name(int(msgid))
                    
                    self.tree.insert("", "end", values=(i + 1, time, src, dst, proto, command_name))
            except Exception as e:
                print(f"Error parsing packet {i}: {e}")
    
    def apply_filter(self):
        protocol_filter = self.protocol_entry.get().strip()
        src_filter = self.src_entry.get().strip()
        dst_filter = self.dst_entry.get().strip()
        command_filter = self.msgid_entry.get().strip().lower()
        
        self.tree.delete(*self.tree.get_children())
        
        if not self.capture:
            return
        
        for i, packet in enumerate(self.capture):
            try:
                if "IP" in packet:
                    src = packet.ip.src
                    dst = packet.ip.dst
                    proto = packet.highest_layer
                    time = packet.sniff_time.strftime("%H:%M:%S.%f")
                    
                    # Extract MsgID from MAVLINK_PROTO layer
                    command_name = "N/A"
                    if "MAVLINK_PROTO" in packet:
                        msgid = packet["MAVLINK_PROTO"].get_field_value("msgid")
                        if msgid:
                            command_name = self.get_mavlink_command_name(int(msgid))
                    
                    # Apply filters
                    if protocol_filter and protocol_filter.lower() not in proto.lower():
                        continue
                    if src_filter and src_filter != src:
                        continue
                    if dst_filter and dst_filter != dst:
                        continue
                    if command_filter and command_filter not in command_name.lower():
                        continue
                    
                    self.tree.insert("", "end", values=(i + 1, time, src, dst, proto, command_name))
            except Exception as e:
                print(f"Error filtering packet {i}: {e}")
    
    def display_packet_details(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        packet_index = int(self.tree.item(selected_item, "values")[0]) - 1
        try:
            packet = self.capture[packet_index]
            details = f"Packet {packet_index + 1} Details:\n\n"
            
            for layer in packet.layers:
                details += f"Layer: {layer.layer_name.upper()}\n"
                for field in layer.field_names:
                    field_value = layer.get_field_value(field)
                    details += f"  {field.replace('_', ' ').capitalize()}: {field_value}\n"
                details += "\n"
            
            self.detail_text.delete(1.0, tk.END)
            self.detail_text.insert(tk.END, details)
        except Exception as e:
            self.detail_text.delete(1.0, tk.END)
            self.detail_text.insert(tk.END, f"Error displaying packet details: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PacketFilterApp(root)
    root.mainloop()

import psutil
import platform
import socket
import uuid
import cpuinfo
import subprocess


class systeminfo:
    def __init__(self):
        self.name = "systeminfo"
        self.info = "Gives Basic System Information of File"
        self.args = []
        self.command = ":systeminfo"

    def systeminfo_template(self,system_info, installed_software):
        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Courier New', Courier, monospace;
                    background-color: #1e1e1e;
                    color: #ffffff;
                    padding: 20px;
                }}
                .container {{
                    width: 90%;
                    margin: 0 auto;
                }}
                .header {{
                    color: #00ff00;
                    font-size: 24px;
                    margin-bottom: 20px;
                }}
                .section {{
                    margin-bottom: 20px;
                }}
                .section-title {{
                    color: #ff4500;
                    font-size: 20px;
                    border-bottom: 1px solid #3c3c3c;
                    padding-bottom: 5px;
                    margin-bottom: 10px;
                }}
                .section-content pre {{
                    color: #FFFF99;
                    background-color: #252526;
                    padding: 10px;
                    border-radius: 5px;
                    white-space: pre-wrap;
                    
                }}
                .installed-software ul {{
                    list-style-type: none;
                    padding: 0;
                }}
                .installed-software li {{
                    background-color: #252526;
                    margin: 5px 0;
                    padding: 5px 10px;
                    border-radius: 5px;
                    color: #ffffff;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">System Information Report</div>
                <div class="section">
                    <div class="section-title">System Information</div>
                    <div class="section-content">
                    <pre>
                    {system_info}
                    </pre></div>
                </div>
                <div class="section">
                    <div class="section-title">Installed Software</div>
                    <div class="section-content installed-software">
                        <ul>
        """
        for software in installed_software[:20]:
            html_content += f"<li>{software}</li>"

        html_content += """
                        </ul>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content

    def get_size(self, bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def get_installed_software(self):
        installed_software = []
        system = platform.system()

        if system == "Windows":
            try:
                import winreg
                def get_software_from_registry(hive, flag):
                    registry = winreg.ConnectRegistry(None, hive)
                    uninstall_key = winreg.OpenKey(registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | flag)
                    count = winreg.QueryInfoKey(uninstall_key)[0]
                    software_list = []
                    for i in range(count):
                        try:
                            key_name = winreg.EnumKey(uninstall_key, i)
                            software_key = winreg.OpenKey(uninstall_key, key_name)
                            display_name = winreg.QueryValueEx(software_key, "DisplayName")[0]
                            software_list.append(display_name)
                        except WindowsError:
                            continue
                    return software_list

                installed_software = get_software_from_registry(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY)
                installed_software += get_software_from_registry(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY)
                installed_software += get_software_from_registry(winreg.HKEY_CURRENT_USER, 0)
            except ImportError:
                installed_software.append("Unable to retrieve software list on Windows.")

        elif system == "Darwin":  # macOS
            try:
                output = subprocess.check_output(["system_profiler", "SPApplicationsDataType", "-detailLevel", "mini"]).decode("utf-8")
                for line in output.split('\n'):
                    if ':' in line:
                        app = line.split(':')[1].strip()
                        if app:
                            installed_software.append(app)
            except subprocess.CalledProcessError:
                installed_software.append("Unable to retrieve software list on macOS.")

        elif system == "Linux":
            try:
                if subprocess.call(["which", "dpkg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                    output = subprocess.check_output(["dpkg", "--get-selections"]).decode("utf-8")
                    installed_software = [line.split()[0] for line in output.split('\n') if line and not line.endswith("deinstall")]
                elif subprocess.call(["which", "rpm"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                    output = subprocess.check_output(["rpm", "-qa"]).decode("utf-8")
                    installed_software = output.split('\n')
                elif subprocess.call(["which", "pacman"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                    output = subprocess.check_output(["pacman", "-Qq"]).decode("utf-8")
                    installed_software = output.split('\n')
                else:
                    installed_software.append("Unable to retrieve software list on this Linux distribution.")
            except subprocess.CalledProcessError:
                installed_software.append("Unable to retrieve software list on Linux.")

        else:
            installed_software.append(f"Software list retrieval not supported on {system}")

        return installed_software

    def get_system_info(self):
        info = []
        info.append("="*40 + " System Information " + "="*40)
        uname = platform.uname()
        info.append(f"System: {uname.system}")
        info.append(f"Node Name: {uname.node}")
        info.append(f"Release: {uname.release}")
        info.append(f"Version: {uname.version}")
        info.append(f"Machine: {uname.machine}")
        info.append(f"Processor: {uname.processor}")

        info.append("\n" + "="*40 + " CPU Info " + "="*40)
        info.append(f"Physical cores: {psutil.cpu_count(logical=False)}")
        info.append(f"Total cores: {psutil.cpu_count(logical=True)}")
        cpu_freq = psutil.cpu_freq()
        info.append(f"Max Frequency: {cpu_freq.max:.2f}Mhz")
        info.append(f"Min Frequency: {cpu_freq.min:.2f}Mhz")
        info.append(f"Current Frequency: {cpu_freq.current:.2f}Mhz")
        info.append("CPU Usage Per Core:")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            info.append(f"Core {i}: {percentage}%")
        info.append(f"Total CPU Usage: {psutil.cpu_percent()}%")

        info.append("\n" + "="*40 + " Memory Information " + "="*40)
        svmem = psutil.virtual_memory()
        info.append(f"Total: {self.get_size(svmem.total)}")
        info.append(f"Available: {self.get_size(svmem.available)}")
        info.append(f"Used: {self.get_size(svmem.used)}")
        info.append(f"Percentage: {svmem.percent}%")

        info.append("\n" + "="*40 + " Disk Information " + "="*40)
        partitions = psutil.disk_partitions()
        for partition in partitions:
            info.append(f"=== Device: {partition.device} ===")
            info.append(f"  Mountpoint: {partition.mountpoint}")
            info.append(f"  File system type: {partition.fstype}")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            info.append(f"  Total Size: {self.get_size(partition_usage.total)}")
            info.append(f"  Used: {self.get_size(partition_usage.used)}")
            info.append(f"  Free: {self.get_size(partition_usage.free)}")
            info.append(f"  Percentage: {partition_usage.percent}%")

        info.append("\n" + "="*40 + " Network Information " + "="*40)
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                info.append(f"=== Interface: {interface_name} ===")
                if str(address.family) == 'AddressFamily.AF_INET':
                    info.append(f"  IP Address: {address.address}")
                    info.append(f"  Netmask: {address.netmask}")
                    info.append(f"  Broadcast IP: {address.broadcast}")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    info.append(f"  MAC Address: {address.address}")
                    info.append(f"  Netmask: {address.netmask}")
                    info.append(f"  Broadcast MAC: {address.broadcast}")

        info.append("\n" + "="*40 + " Additional System Information " + "="*40)
        info.append(f"Hostname: {socket.gethostname()}")
        info.append(f"IP Address: {socket.gethostbyname(socket.gethostname())}")
        info.append(f"Mac Address: {':'.join(('%012x' % uuid.getnode())[i:i+2] for i in range(0, 12, 2))}")
        info.append(f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}")

        return "\n".join(info)
    
    def run(self,EmailHandler,msgId):
        system_info = self.get_system_info()
        installed_software = self.get_installed_software()
        html_content = self.systeminfo_template(system_info, installed_software)
        EmailHandler.send_email(
            message=html_content,
            msgId=msgId,
            reply=True,
        )

if __name__ == "__main__":
    sys = systeminfo()
    system_info = sys.get_system_info()
    installed_software = sys.get_installed_software()
    html_content = systeminfo_template(system_info, installed_software)
    print(html_content)  # You can comment this out if you don't want to print

    # Example of how you might use this to send an email
    # (You'd need to set up the email sending functionality)
    # send_email("recipient@example.com", "System Information", html_content)

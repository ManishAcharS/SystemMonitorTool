import os
import platform
import sys

CRON_TEMPLATE = """# SysGuard auto-monitoring cron job (runs every minute)
* * * * * cd {workdir} && {python} monitor.py >> sysguard.log 2>&1
"""


TASK_XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{python}</Command>
      <Arguments>monitor.py</Arguments>
      <WorkingDirectory>{workdir}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"""


def main():
    workdir = os.path.abspath(os.getcwd())
    py = sys.executable
    system = platform.system()

    if system == "Windows":
        xml = TASK_XML_TEMPLATE.format(python=py, workdir=workdir)
        out = os.path.join(workdir, "sysguard_task.xml")
        with open(out, "w", encoding="utf-16le") as f:
            f.write(xml)
        print("Generated sysguard_task.xml")
        print("Import it with Task Scheduler: schtasks /Create /XML sysguard_task.xml /TN SysGuard")
        return
    if system == "Linux":
        cron = CRON_TEMPLATE.format(workdir=workdir, python=py)
        out = os.path.join(workdir, "sysguard_cron.txt")
        with open(out, "w", encoding="utf-8") as f:
            f.write(cron)
        print("Generated sysguard_cron.txt")
        print("Install: crontab sysguard_cron.txt")
        return
    print(f"Unsupported OS: {system}. Generated templates skipped.")


if __name__ == "__main__":
    main()

![Banner](banner.png)

# File Access Control Analysis Tool: `file-access-control`

## 1. Overview

`file-access-control` is a command-line tool that lists and changes the permission mode of a file or directory. It lists the current octal mode, sets a requested mode with os.chmod, and removes permission bits. It does not manage access control lists, perform compliance checks, or validate permissions against a policy: no such code is in this tool.


## 2. Analysis Purposes

This tool serves the following security analysis purposes:

* **Mode listing:** Prints the current octal permission mode of the named path.
* **Setting a mode:** `--set-permissions USER PERMISSIONS` applies the requested mode. An octal value such as 640 is applied as the full mode; a set of bits such as rwx sets the owner bits. The before and after modes are reported.
* **Removing permissions:** `--remove-permissions USER` removes permissions. A set of bits such as rw clears those bits from the mode; any other value clears all owner permission bits for the named user. The before and after modes are reported.

A run naming a missing path exits 1. A run naming no operation exits 1 with a line requiring one operation.

## 3. Installation

**Prerequisites:** Python 3.7+ and the following packages:

* `argparse>=1.4.0`
* `pathlib` (typically included with Python 3.4+)
* `logging` (typically included with Python)

**Installation Steps:**

1.  Clone the repository:  `git clone <repository_url>` (Replace `<repository_url>` with the actual repository URL).
2.  Navigate to the project directory: `cd file-access-control`
3.  Install dependencies: `pip install -r requirements.txt` (assuming a `requirements.txt` file is present listing the dependencies).

## 4. Usage

The tool utilizes a command-line interface driven by `argparse`.  The following arguments are supported (further details will be provided in the future):

**(Note:  This section will be fleshed out as the tool's capabilities are fully defined.)**


**Basic Usage:**

```bash
python main.py <path> --list-permissions
```

* `<path>`: The path to the file or directory to manage permissions for.
* `--list-permissions`:  (Optional) List current permissions for the file or directory.
* `--set-permissions USER PERMISSIONS`: (Optional) Set permissions for a specific user.
* `--remove-permissions USER`: (Optional) Remove all permissions for a specific user.


**Example with Safeguards:**

Listing the current permissions of a specific directory:

```bash
python main.py /home/user/sensitive_data --list-permissions
```

**Important Safeguards:**

* Always run the tool with appropriate privileges.  Avoid running with root/administrator privileges unless absolutely necessary.
* Verify the integrity of the tool's source code before execution.
* Carefully review the listed permissions to identify and address potential vulnerabilities.


## 5. Implementation Details (Security Focused)

* **Path check:** The named path must exist; a missing path exits 1.
* **Mode changes:** Mode changes are made with os.chmod and the before and after modes are logged.
* **Logging:** Actions and mode changes are logged with timestamps.


## 6. Modules and Core Functions

The tool's core functionality is implemented in `main.py`.

* **`setup_argparse()`:** This function configures the command-line interface using `argparse`.
* **`main()`:** This function handles command-line argument parsing, performs the file access control analysis, and prints the current permissions.


## 7. License


This software is licensed under the MIT License.


## 8. Future Development

Future development will include:

* More sophisticated reporting capabilities.
* Support for different operating systems and file systems.
* Integration with other security tools.


This documentation will be updated as the tool evolves.
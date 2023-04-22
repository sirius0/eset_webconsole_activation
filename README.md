# ESET Web Console Activation

This Python script automates the activation process for ESET Web Console by uploading a license file to the server. It takes care of creating a symbolic link, initializing the necessary libraries, and making API calls to authenticate and add the license to the server.

## Prerequisites

Make sure you have Python 3 installed on your system. You can check your Python version by running:

```bash
python3 --version
```

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/sirius0/eset_webconsole_activation.git
```

2. Change to the `eset_webconsole_activation` directory:

```bash
cd eset_webconsole_activation
```

## Usage

To run the script, execute the following command:

```bash
python3 eset_webconsole_activation.py <username> <password> <ERAServer port> <licence file>
```

Replace `<username>`, `<password>`, `<ERAServer port>` and `<licence file>` with your ESET Web Console credentials, ERA server port and the path to your license file.

For example:

```bash
python3 eset_webconsole_activation.py admin password123 /path/to/license_file.lf
```

The script will perform the following steps:

1. Create a symbolic link if it does not exist.
2. Load the necessary libraries and initialize them.
3. Authenticate with the provided username and password.
4. Add the license to the server using the provided license file.

You will see output messages indicating the progress and success of each step.

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes. We appreciate your contributions!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

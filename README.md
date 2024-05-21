# PC Part Scrapper MX

PC Part Scrapper MX is a tool designed to scrape data about PC components from various Mexican online stores. This project aims to provide users with up-to-date information on prices of PC parts based on a list of parts and search queries. I used this scrapper to build my own PC. Hope it could help someone!

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## Features

- Scrapes data from multiple Mexican online stores such as: Amazon, Cyberpuerta, Google
- Provides detailed information on PC components such as prices and the link of the source
- Outputs data in a user-friendly format (TSV)
- Error handling and logging

## Installation

To get started with PC Part Scrapper MX, follow these steps:

1. **Clone the repository:**
   ```sh
   git clone https://github.com/LukeCepza/PC_Part_Scrapper_Mx.git
   cd PC_Part_Scrapper_Mx
   ```

2. **Install the required dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

To run the scrapper, use the following commands:

```sh
python scrapper.py
python app.py
```

`scrapper.py` fetches the data from the internet. It may take a while, around 17 minutes.

`app.py` displays the information in a very basic web-based GUI to see the different options based on the cheapest options found.

To personalize the query you can modify the dictionary:

```python
components = {
        "SSD": "SSD 2TB",
        "RAM": "DDR5 RAM 64 Gb",
        "COOL": "MSI MAG CORELIQUID E360",
        "PSU": "PSU 850W 80 PLUS Gold",
        "CPU": "AMD 7950X",
        "MB": "Tarjeta madre AM5 AMD",
        "GPU": "4070 Ti Super",
        "GAB": "Gabinete computadora ATX"
}
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or feedback, please contact [lkcepza@gmail.com](mailto:lkcepza@gmail.com).


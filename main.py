from PC_parts_scrapper import get_data_amazon, get_data_cyberpuerta, get_data_google_shopping, clean_price
import pandas as pd
#https://pcreathors.mx/producto/ma11-equipo-amd-ryzen-9-7950x-64gb-ram-rtx-4080-super-aero-oc-2tb-ssd

def scrape(components, csv = ''):
    
    websites = {
        "Amazon": "https://www.amazon.com.mx/s?k=",
        "Cyberpuerta": "https://www.cyberpuerta.mx/index.php?cl=search&searchparam=",
        "Google" : "https://www.google.com/search?tbm=shop&q="
    }

    data = []
    data = get_data_amazon(data, components, websites)
    data = get_data_cyberpuerta(data, components, websites)
    data = get_data_google_shopping(data, components, websites)

    df = pd.DataFrame(data, columns=['location', 'part', 'query','price','full',  'link'])

    # Apply the clean_price function to the Price column
    df['price'] = df['price'].apply(clean_price)
    df = df.dropna()
    if csv: 
        previous_df = pd.read_csv(csv, sep='\t')
        df = pd.concat([previous_df, df], ignore_index=True)
    df.to_csv('computer_components.tsv', sep='\t', index=False)

    return df

if __name__ == '__main__':
    
    components = {
        "CPU": "AMD 7950X",
        "MB": "Tarjeta madre AM5 AMD",
        "GPU": "4070 Ti Super",
        "GAB": "Gabinete computadora ATX",
    }
    scrape(components)
    components = {
        "SSD": "SSD 2TB",
        "RAM": "DDR5 RAM 64 Gb",
        "COOL": "MSI MAG CORELIQUID E360",
        "PSU": "PSU 850W 80 PLUS Gold"
    }
    scrape(components, csv = 'computer_components.tsv')
    components = {
        "CPU": "Intel Core i7 14700",
        "MB": "Tarjeta madre LGA1700 INTEL",
        "GPU": "4070 Ti",
        "SSD": "SSD 4TB",
    }
    scrape(components, csv = 'computer_components.tsv')
    components = {
        "GPU": "4070 Super",
        "GAB": "Gabinete Midi-Tower",
        "RAM": "DDR5 RAM 32 Gb",
        "COOL": "Corsair iCUE Link H150i RGB",
    }
    scrape(components, csv = 'computer_components.tsv')
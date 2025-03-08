import requests
from typing import Dict, Optional, Any
from tabulate import tabulate
from colorama import init, Fore, Style
import sys

# Initialize colorama
init(autoreset=True)

class CountryExplorer:
    """
    A tool for exploring and comparing countries worldwide.
    Built with love for geography enthusiasts and travelers.
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://restcountries.com/v3.1"
        
    def show_error(self, msg: str) -> None:
        print(f"{Fore.RED}❌ {msg}{Style.RESET_ALL}")

    def show_success(self, msg: str) -> None:
        print(f"{Fore.GREEN}✨ {msg}{Style.RESET_ALL}")

    def clean_country_name(self, raw_name: str) -> str:
        return raw_name.strip().lower().title()

    def fetch_country_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Fetches detailed information about a country.
        Handles API communication and data processing.
        """
        try:
            response = self.session.get(
                f"{self.base_url}/name/{name}",
                timeout=10
            )
            response.raise_for_status()
            
            raw_data = response.json()
            if not raw_data or not isinstance(raw_data, list):
                return None
                
            country = raw_data[0]
            
            # Process currency information
            currency_details = []
            for code, info in country.get("currencies", {}).items():
                currency_name = info.get("name", "Unknown")
                currency_details.append(f"{code} ({currency_name})")
            
            # Get neighboring countries
            neighbors = country.get("borders", [])
            neighbor_list = ", ".join(neighbors) if neighbors else "No bordering countries"

            # Process spoken languages
            spoken_langs = list(country.get("languages", {}).values())
            lang_list = ", ".join(spoken_langs) if spoken_langs else "Data unavailable"

            # Build country profile
            profile = {
                "Name": country.get("name", {}).get("common", "Unknown"),
                "Official Name": country.get("name", {}).get("official", "Unknown"),
                "Capital": country.get("capital", ["Unknown"])[0],
                "Region": country.get("region", "Unknown"),
                "Subregion": country.get("subregion", "Unknown"),
                "Population": f"{country.get('population', 0):,} people",
                "Land Area": f"{country.get('area', 0):,} km²",
                "Currencies": ", ".join(currency_details),
                "Languages": lang_list,
                "Time Zones": ", ".join(country.get("timezones", [])),
                "Neighboring Countries": neighbor_list,
                "Flag": f"{country.get('flag', '🏳')} {country.get('name', {}).get('common', '')}"
            }
            
            return profile
                
        except requests.RequestException as e:
            self.show_error(f"Couldn't fetch data for {name} (Network error: {str(e)})")
        except Exception as e:
            self.show_error(f"Something went wrong while processing {name} ({str(e)})")
        return None

    def compare(self, first_country: str, second_country: str) -> None:
        """
        Creates a side-by-side comparison of two countries.
        Presents data in a clean, easy-to-read format.
        """
        print(f"\n🔍 Finding information about {first_country} and {second_country}...")
        
        first_data = self.fetch_country_info(first_country)
        second_data = self.fetch_country_info(second_country)
        
        if not first_data or not second_data:
            self.show_error("Couldn't get complete information for comparison")
            return
        
        comparison_data = []
        headers = ["Category", first_country.upper(), second_country.upper()]
        
        for key in first_data.keys():
            row = [
                f"{Fore.CYAN}{key}{Style.RESET_ALL}",
                str(first_data[key]),
                str(second_data[key])
            ]
            comparison_data.append(row)
        
        print("\n" + "=" * 80)
        print(f"{Fore.YELLOW}🌍 Comparing: {first_country.upper()} vs {second_country.upper()}{Style.RESET_ALL}")
        print("=" * 80 + "\n")
        
        print(tabulate(comparison_data, headers=headers, tablefmt="grid"))
        print("\n🌐 Data provided by REST Countries API")

def explore_countries():
    """
    Interactive country exploration tool.
    Perfect for learning about different nations and making comparisons.
    """
    explorer = CountryExplorer()
    
    print(f"{Fore.CYAN}🌍 Welcome to Country Explorer!{Style.RESET_ALL}")
    print("Discover and compare countries around the world.\n")
    
    while True:
        try:
            first = input(f"{Fore.YELLOW}First country to explore{Style.RESET_ALL}: ").strip()
            second = input(f"{Fore.YELLOW}Second country to explore{Style.RESET_ALL}: ").strip()
            
            if not first or not second:
                explorer.show_error("Please enter both country names!")
                continue
                
            first = explorer.clean_country_name(first)
            second = explorer.clean_country_name(second)
            
            explorer.compare(first, second)
            
            another = input(f"\n{Fore.YELLOW}Would you like to explore more countries? (y/n):{Style.RESET_ALL} ").lower()
            if another != 'y':
                explorer.show_success("Thanks for exploring with us! Safe travels! 🌎")
                break
                
        except KeyboardInterrupt:
            print("\n\nExploration ended by user. Goodbye! 👋")
            sys.exit(0)
        except Exception as e:
            explorer.show_error(f"Oops! Something unexpected happened: {str(e)}")
            continue

if __name__ == "__main__":
    explore_countries()

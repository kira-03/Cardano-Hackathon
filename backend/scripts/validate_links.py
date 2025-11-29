"""
Link Validator - Verify all external URLs in the application
Ensures no 404 errors on any resource links
"""
import asyncio
import aiohttp
from typing import List, Dict, Tuple
from colorama import init, Fore, Style

init(autoreset=True)

# All external links used in PDF generation and documentation
LINKS_TO_VALIDATE = {
    "DEX Platforms": [
        "https://minswap.org",
        "https://muesliswap.com",
        "https://app.wingriders.com",
        "https://sundaeswap.finance",
    ],
    "Block Explorers": [
        "https://cardanoscan.io",
        "https://cexplorer.io",
        "https://pool.pm",
    ],
    "Exchanges": [
        "https://www.binance.com/en/support/announcement/new-cryptocurrency-listing",
        "https://www.coinbase.com/cloud/discover/dev-foundations/listing-an-asset",
        "https://support.kraken.com/hc/en-us/articles/360001388206",
        "https://www.kucoin.com/support/360002511932",
        "https://www.gate.io/en/article/16194",
    ],
    "Bridge Services": [
        "https://li.fi",
        "https://axelar.network",
        "https://www.multichain.org",
        "https://cbridge.celer.network",
    ],
    "Cardano Resources": [
        "https://cardano.org",
        "https://developers.cardano.org",
        "https://docs.cardano.org",
        "https://forum.cardano.org",
    ],
    "API Services": [
        "https://blockfrost.io",
        "https://www.coinpaprika.com",
        "https://www.coingecko.com",
    ],
    "Documentation": [
        "https://github.com/cardano-foundation",
        "https://cips.cardano.org",
    ]
}

async def check_url(session: aiohttp.ClientSession, url: str) -> Tuple[str, int, str]:
    """
    Check if a URL is accessible
    
    Returns:
        Tuple of (url, status_code, status_message)
    """
    try:
        async with session.head(url, timeout=aiohttp.ClientTimeout(total=10), allow_redirects=True) as response:
            return (url, response.status, "OK" if response.status == 200 else f"Status {response.status}")
    except asyncio.TimeoutError:
        return (url, 0, "TIMEOUT")
    except aiohttp.ClientError as e:
        return (url, 0, f"ERROR: {str(e)[:50]}")
    except Exception as e:
        return (url, 0, f"EXCEPTION: {str(e)[:50]}")

async def validate_links() -> Dict[str, List[Dict[str, any]]]:
    """
    Validate all external links
    
    Returns:
        Dictionary with validation results per category
    """
    results = {}
    
    async with aiohttp.ClientSession() as session:
        for category, urls in LINKS_TO_VALIDATE.items():
            print(f"\n{Fore.CYAN}Checking {category}...{Style.RESET_ALL}")
            
            tasks = [check_url(session, url) for url in urls]
            responses = await asyncio.gather(*tasks)
            
            category_results = []
            for url, status, message in responses:
                result = {
                    "url": url,
                    "status": status,
                    "message": message,
                    "valid": status == 200
                }
                category_results.append(result)
                
                # Print result
                if result["valid"]:
                    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {url}")
                else:
                    print(f"  {Fore.RED}✗{Style.RESET_ALL} {url} - {message}")
            
            results[category] = category_results
    
    return results

def print_summary(results: Dict[str, List[Dict[str, any]]]):
    """Print validation summary"""
    print(f"\n{'='*80}")
    print(f"{Fore.CYAN}VALIDATION SUMMARY{Style.RESET_ALL}")
    print(f"{'='*80}\n")
    
    total_urls = 0
    valid_urls = 0
    failed_urls = []
    
    for category, category_results in results.items():
        total = len(category_results)
        valid = sum(1 for r in category_results if r["valid"])
        failed = [r for r in category_results if not r["valid"]]
        
        total_urls += total
        valid_urls += valid
        
        if failed:
            failed_urls.extend([(category, r) for r in failed])
        
        status_color = Fore.GREEN if valid == total else Fore.YELLOW
        print(f"{status_color}{category}: {valid}/{total} valid{Style.RESET_ALL}")
    
    print(f"\n{'='*80}")
    print(f"Total URLs: {total_urls}")
    print(f"{Fore.GREEN}Valid: {valid_urls}{Style.RESET_ALL}")
    print(f"{Fore.RED}Failed: {len(failed_urls)}{Style.RESET_ALL}")
    print(f"{'='*80}\n")
    
    if failed_urls:
        print(f"{Fore.RED}FAILED URLS:{Style.RESET_ALL}\n")
        for category, result in failed_urls:
            print(f"  [{category}] {result['url']}")
            print(f"    → {result['message']}\n")
    else:
        print(f"{Fore.GREEN}🎉 All links validated successfully!{Style.RESET_ALL}\n")

async def main():
    """Main validation function"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print("LINK VALIDATOR - EcosystemBridge Assistant")
    print(f"{'='*80}{Style.RESET_ALL}\n")
    print("Validating all external resource links...")
    
    results = await validate_links()
    print_summary(results)
    
    # Return exit code
    all_valid = all(
        all(r["valid"] for r in category_results)
        for category_results in results.values()
    )
    return 0 if all_valid else 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Validation interrupted by user{Style.RESET_ALL}")
        exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        exit(1)

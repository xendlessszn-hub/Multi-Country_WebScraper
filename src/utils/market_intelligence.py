"""
Market Intelligence Module - TAM/SAM/SOM calculation - Competitive landscape - Growth projections
"""

import pandas as pd
import numpy as np

class MarketIntelligence:
    def __init__(self, df):
        self.df = df

    def calculate_tam_sam_som(self):
        """
        TAM: Total Addressable Market (all agencies)
        SAM: Serviceable Available Market (fit score >= 5)
        SOM: Serviceable Obtainable Market (fit score >= 7, realistic capture)
        """
        # TAM: Total potential revenue from all partners
        tam = self.df['revenue_usd'].sum()

        # SAM: Partners with medium+ fit
        sam_partners = self.df[self.df['kaycore_fit_score'] >= 5]
        sam = sam_partners['revenue_usd'].sum()

        # SOM: High-priority partners, assume 15% revenue share
        som_partners = self.df[self.df['kaycore_fit_score'] >= 7]
        som = som_partners['revenue_usd'].sum() * 0.15  # 15% revenue share assumption

        return {
            'tam_usd': tam,
            'sam_usd': sam,
            'som_usd': som,
            'tam_partners': len(self.df),
            'sam_partners': len(sam_partners),
            'som_partners': len(som_partners)
        }

    def project_revenue_growth(self, target_partners=50, avg_deal_size=50000):
        """
        Project 50% revenue growth scenario
        Assumptions:
        - Partner with 50 agencies in Year 1
        - Avg deal: $50K (SecureShield + services)
        - Recurring revenue: 70%
        """
        year1_revenue = target_partners * avg_deal_size
        year2_revenue = year1_revenue * 1.5  # 50% growth target
        year3_revenue = year2_revenue * 1.3  # Sustained growth

        return {
            'year1_revenue': year1_revenue,
            'year2_revenue': year2_revenue,
            'year3_revenue': year3_revenue,
            'year1_partners': target_partners,
            'year2_partners': int(target_partners * 1.3),
            'year3_partners': int(target_partners * 1.6)
        }

    def analyze_by_country(self):
        """Country-level market analysis"""
        country_stats = self.df.groupby('country').agg({
            'revenue_usd': ['sum', 'mean', 'count'],
            'kaycore_fit_score': 'mean',
            'partnership_priority': lambda x: (x == 'High').sum()
        }).round(2)

        country_stats.columns = [
            'total_revenue',
            'avg_revenue',
            'num_partners',
            'avg_fit_score',
            'high_priority_count'
        ]

        return country_stats

    def generate_report(self):
        """Generate comprehensive market report"""
        tam_sam_som = self.calculate_tam_sam_som()
        growth_proj = self.project_revenue_growth()
        country_analysis = self.analyze_by_country()

        report = {
            'market_sizing': tam_sam_som,
            'growth_projection': growth_proj,
            'country_breakdown': country_analysis
        }

        # Save to file
        pd.Series(tam_sam_som).to_csv('data/processed/market_sizing.csv')
        pd.Series(growth_proj).to_csv('data/processed/growth_projection.csv')
        country_analysis.to_csv('data/processed/country_analysis.csv')

        return report


# Generate report
if __name__ == "__main__":
    df = pd.read_csv('data/processed/partners_with_clusters.csv')
    mi = MarketIntelligence(df)
    report = mi.generate_report()

    print("\n" + "="*60)
    print("KAYCORE GLOBAL PARTNERSHIP - MARKET INTELLIGENCE REPORT")
    print("="*60)

    print("\n MARKET SIZING:")
    print(f"TAM (Total Market): ${report['market_sizing']['tam_usd']:,.0f} from {report['market_sizing']['tam_partners']} partners")
    print(f"SAM (Target Market): ${report['market_sizing']['sam_usd']:,.0f} from {report['market_sizing']['sam_partners']} partners")
    print(f"SOM (Obtainable): ${report['market_sizing']['som_usd']:,.0f} from {report['market_sizing']['som_partners']} partners")

    print("\n REVENUE GROWTH PROJECTION (50% Target):")
    print(f"Year 1: ${report['growth_projection']['year1_revenue']:,.0f} ({report['growth_projection']['year1_partners']} partners)")
    print(f"Year 2: ${report['growth_projection']['year2_revenue']:,.0f} ({report['growth_projection']['year2_partners']} partners)")
    print(f"Year 3: ${report['growth_projection']['year3_revenue']:,.0f} ({report['growth_projection']['year3_partners']} partners)")

    print("\n COUNTRY BREAKDOWN:")
    print(report['country_breakdown'])
    print("="*60)

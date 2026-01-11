import streamlit as st
import json
import pandas as pd
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page Config
st.set_page_config(
    page_title="FedEx SmartRecover",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #660099;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #666666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #660099;
    }
    .manual-review {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    .legal-case {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Paths
def get_data_path():
    """Get path to processed allocations"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '../1_AI_Model_Engine/processed_allocations.json')
    if not os.path.exists(json_path):
        # Try alternative path
        json_path = os.path.join(current_dir, '..', '1_AI_Model_Engine', 'processed_allocations.json')
    return json_path

def load_data():
    """Load data from AI engine output"""
    json_path = get_data_path()
    
    if not os.path.exists(json_path):
        # Create sample data if file doesn't exist
        st.warning("⚠️ No data found. Running AI engine to generate sample data...")
        try:
            # Import and run the AI engine
            import subprocess
            ai_engine_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                         '1_AI_Model_Engine', 'ai_engine.py')
            result = subprocess.run(['python', ai_engine_path], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                st.success("✅ AI engine executed successfully!")
            else:
                st.error(f"❌ Error running AI engine: {result.stderr}")
                return None
        except Exception as e:
            st.error(f"❌ Could not run AI engine: {e}")
            return None
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return None

def format_currency(value):
    """Format currency values"""
    if isinstance(value, str):
        return value
    return f"${value:,.2f}"

def create_visualizations(df):
    """Create charts and visualizations"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Agency distribution pie chart
        agency_counts = df['assigned_agency'].value_counts()
        st.markdown("#### 📊 Agency Distribution")
        st.bar_chart(agency_counts)
    
    with col2:
        # P2P Score distribution
        st.markdown("#### 📈 P2P Score Distribution")
        st.line_chart(df['p2p_score'])

def main():
    # --- HEADER ---
    st.markdown('<p class="main-header">📦 FedEx SmartRecover Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Intelligent Debt Collection Allocation & Governance Portal</p>', unsafe_allow_html=True)
    st.divider()
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("### 🎯 Filters")
        
        # Auto-run option
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This dashboard displays AI-optimized debt allocation decisions from the SmartRecover engine.
        
        **Key Features:**
        - Real-time allocation tracking
        - Confidence-based governance
        - ROI and performance analytics
        """)
    
    # --- LOAD DATA ---
    data = load_data()
    
    if not data:
        st.error("""
        Unable to load data. Please ensure:
        1. The AI engine has been run (`python 1_AI_Model_Engine/ai_engine.py`)
        2. `processed_allocations.json` exists in the correct location
        """)
        
        if st.button("📊 Generate Sample Data", type="primary"):
            # Create sample data structure
            sample_data = {
                "meta": {
                    "timestamp": datetime.now().isoformat(),
                    "version": "SmartRecover v2.0",
                    "kpis": {
                        "Portfolio_Value": "$85,000",
                        "Expected_Recovery_Value": "$62,000",
                        "Commission_Savings_90d": "$18,000",
                        "Auto_Allocation_Rate": "85.7%",
                        "High_Risk_Cases": 1,
                        "Avg_Confidence_Score": "0.82"
                    },
                    "governance_flags": {
                        "data_quality_score": 0.94,
                        "fairness_variance": 0.08,
                        "retraining_eligible": True
                    }
                },
                "allocations": [
                    {
                        "tokenized_id": "FED-8A7B3C9D",
                        "amount": 12500,
                        "p2p_score": 72.4,
                        "assigned_agency": "FedEx Internal Team",
                        "p2p_confidence": 0.89,
                        "requires_manual_review": False
                    },
                    {
                        "tokenized_id": "FED-5E6F7A8B",
                        "amount": 45000,
                        "p2p_score": 35.2,
                        "assigned_agency": "DCA_Alpha_Legal",
                        "p2p_confidence": 0.91,
                        "requires_manual_review": False
                    },
                    {
                        "tokenized_id": "FED-1C2D3E4F",
                        "amount": 300,
                        "p2p_score": 58.5,
                        "assigned_agency": "DCA_Beta_Digital",
                        "p2p_confidence": 0.78,
                        "requires_manual_review": False
                    }
                ]
            }
            
            # Save sample data
            json_path = get_data_path()
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, 'w') as f:
                json.dump(sample_data, f, indent=2)
            
            st.success("✅ Sample data generated! Refresh the page to view.")
            st.rerun()
        return
    
    # --- KPI SECTION ---
    st.subheader("📊 Executive Summary (90-Day Projection)")
    
    kpis = data['meta']['kpis']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Commission Savings", 
            value=kpis['Commission_Savings_90d'],
            delta="30% vs Manual Process",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="🤖 Auto-Allocation Rate", 
            value=kpis['Auto_Allocation_Rate'],
            delta="99.5% Speedup",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="📉 Portfolio Value", 
            value=kpis['Portfolio_Value']
        )
    
    with col4:
        st.metric(
            label="🧠 Avg. Confidence", 
            value=kpis['Avg_Confidence_Score']
        )
    
    st.divider()
    
    # --- MAIN TABLE ---
    st.subheader("📋 Live Allocation Feed")
    
    # Convert allocations list to DataFrame
    df = pd.DataFrame(data['allocations'])
    
    # Add status indicators
    def get_status_icon(row):
        if row['requires_manual_review']:
            return "⏸️"
        elif row['assigned_agency'] == 'FedEx Internal Team':
            return "🏢"
        elif 'Legal' in row['assigned_agency']:
            return "⚖️"
        elif 'Digital' in row['assigned_agency']:
            return "🤖"
        else:
            return "🤝"
    
    df['Status'] = df.apply(get_status_icon, axis=1)
    
    # Format for display
    display_df = df[[
        'Status', 'tokenized_id', 'amount', 'p2p_score', 
        'p2p_confidence', 'assigned_agency', 'requires_manual_review'
    ]].copy()
    
    display_df.columns = ['Status', 'Account ID (Secure)', 'Amount ($)', 
                         'P2P Score', 'Confidence', 'Assigned Agency', 'Manual Review']
    
    # Styling function
    def highlight_rows(row):
        if row['Manual Review']:
            return ['background-color: #fff3cd'] * len(row)
        elif row['Assigned Agency'] == 'FedEx Internal Team':
            return ['background-color: #d4edda'] * len(row)
        elif 'Legal' in row['Assigned Agency']:
            return ['background-color: #f8d7da'] * len(row)
        else:
            return [''] * len(row)
    
    # Display dataframe with styling
    styled_df = display_df.style.apply(highlight_rows, axis=1)
    
    # Format columns
    styled_df = styled_df.format({
        'Amount ($)': '${:,.2f}',
        'P2P Score': '{:.1f}',
        'Confidence': '{:.2%}'
    })
    
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # --- VISUALIZATIONS ---
    st.divider()
    create_visualizations(df)
    
    # --- GOVERNANCE SECTION ---
    st.divider()
    
    with st.expander("🛡️ Governance & Compliance Logs", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Compliance Flags")
            governance = data['meta']['governance_flags']
            
            for key, value in governance.items():
                if isinstance(value, bool):
                    icon = "✅" if value else "❌"
                    st.write(f"{icon} {key.replace('_', ' ').title()}: {value}")
                else:
                    st.write(f"📊 {key.replace('_', ' ').title()}: {value}")
        
        with col2:
            st.markdown("#### System Info")
            meta = data['meta']
            st.write(f"**Version:** {meta['version']}")
            st.write(f"**Last Updated:** {meta['timestamp']}")
            st.write(f"**Data Quality Score:** {governance.get('data_quality_score', 'N/A')}")
        
        # Performance metrics
        st.markdown("#### 📈 Performance Metrics")
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            st.metric("High Risk Cases", kpis['High_Risk_Cases'])
        
        with metrics_col2:
            st.metric("Expected Recovery", kpis['Expected_Recovery_Value'])
        
        with metrics_col3:
            efficiency = float(kpis['Auto_Allocation_Rate'].strip('%')) / 100
            st.metric("Process Efficiency", f"{efficiency:.1%}")

if __name__ == "__main__":
    main()
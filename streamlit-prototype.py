#!/usr/bin/env python3
"""
Streamlit Prototype for Amazon Q AWS Programs Toolkit
A web-based UI for the assessment tools
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Amazon Q AWS Programs Toolkit",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #232F3E;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF9900;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎯 Amazon Q AWS Programs Toolkit</h1>', unsafe_allow_html=True)
    st.markdown("Transform your AWS migration and optimization assessments with AI-powered insights")
    
    # Add help and documentation links
    with st.expander("📚 Documentation & Help", expanded=False):
        tab1, tab2, tab3, tab4 = st.tabs(["📖 Getting Started", "🛠️ Tools Guide", "💡 How to Use", "❓ FAQ"])
        
        with tab1:
            st.markdown("""
            ### 📖 Solution Overview
            
            **What This Toolkit Does:**
            - **Automated Assessment**: Analyzes on-premises infrastructure and recommends AWS equivalents
            - **Cost Optimization**: Identifies licensing savings and right-sizing opportunities  
            - **Infrastructure Deployment**: Automates AWS resource provisioning with best practices
            - **Migration Planning**: Creates phased migration strategies with timeline and cost estimates
            
            **Expected Inputs:**
            - Server inventory CSV with: Server_Name, CPU_Cores, Memory_GB, Storage_GB, OS
            - Windows licensing information (for OLA assessments)
            - Storage usage patterns and requirements
            
            **What It Doesn't Do:**
            - Actual data migration or application cutover
            - Application modernization or code refactoring
            - Network configuration or security setup
            - Staff training or operational procedures
            """)
        
        with tab2:
            st.markdown("""
            ### 🛠️ Available Tools
            
            **Assessment Tools:**
            - **Server Inventory Analyzer** - Maps on-premises servers to AWS services
            - **Windows License Assessment** - Calculates Hybrid Benefit savings
            - **Storage Analysis** - Recommends AWS storage services and migration strategies
            
            **Infrastructure Templates:**
            - **CloudFormation Templates** - VPC, Windows Server, FSx, Active Directory
            - **Automation Scripts** - End-to-end deployment orchestration
            - **Cost Optimization** - Ongoing analysis and recommendations
            
            **Program Support:**
            - **MAP**: Migration Acceleration Program assessments
            - **OLA**: Optimization and Licensing Assessment
            - **ONE OLA**: Windows Server and Storage specializations
            """)
        
        with tab3:
            st.markdown("""
            ### 💡 How to Use This App
            
            **Step-by-Step Guide:**
            1. **Choose Assessment Type** - Select MAP, OLA, or ONE OLA from the sidebar
            2. **Project Setup** - Enter customer information and project parameters
            3. **Upload Data** - Use sample data or upload your server inventory CSV
            4. **Data Validation** - Review data quality and fix any issues
            5. **Run Analysis** - Watch the automated assessment progress
            6. **Review Results** - Explore interactive charts and recommendations
            7. **Export Reports** - Download results for stakeholders
            
            **Pro Tips:**
            - Start with sample data to learn the interface
            - Use the CSV template for proper file formatting
            - Ask Amazon Q for customization help
            - Export results in multiple formats for different audiences
            """)
        
        with tab4:
            st.markdown("""
            ### ❓ Frequently Asked Questions
            
            **Q: What file format should I upload?**
            A: CSV files with columns: Server_Name, CPU_Cores, Memory_GB, Storage_GB, OS, Application_Count, Storage_Type
            
            **Q: Can I test without uploading my own data?**
            A: Yes! Click "Load Sample Data" to try the app with demo data
            
            **Q: How accurate are the cost estimates?**
            A: Estimates are based on current AWS pricing and standard configurations. Actual costs may vary.
            
            **Q: What's the difference between MAP, OLA, and ONE OLA?**
            A: MAP focuses on migration planning, OLA on cost/license optimization, ONE OLA specializes in Windows/Storage
            
            **Q: Can I customize the analysis?**
            A: Yes! Use the Amazon Q chat feature to ask for specific customizations
            
            **Q: Is my data secure?**
            A: Data is processed in memory only and not stored permanently. Sessions are cleared on browser close.
            """)
    
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    # Add help in sidebar too
    with st.sidebar.expander("❓ Quick Help"):
        st.markdown("""
        **🚀 Quick Start:**
        1. Choose assessment type below
        2. Use "Load Sample Data" to test
        3. Follow the step-by-step wizard
        4. Review results and export reports
        
        **📁 CSV Format:**
        Server_Name, CPU_Cores, Memory_GB, Storage_GB, OS
        
        **💡 Pro Tips:**
        - Start with MAP Assessment
        - Try sample data first
        - Use CSV template for uploads
        - Ask Amazon Q for help
        """)
    
    # Add version and links in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Amazon Q AWS Programs Toolkit v1.0**")
    
    # Debug/Reset section
    with st.sidebar.expander("🔧 Debug Tools"):
        if st.button("Reset All Sessions"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("All sessions reset!")
            st.rerun()
        
        st.write("Current session state:")
        for key, value in st.session_state.items():
            st.write(f"- {key}: {value}")
    
    with st.sidebar.expander("📋 About This Tool"):
        st.markdown("""
        **Purpose:** Transform AWS migration and optimization assessments with AI-powered insights
        
        **Programs Supported:**
        - MAP (Migration Acceleration Program)
        - OLA (Optimization & Licensing Assessment)  
        - ONE OLA (Windows & Storage Specialization)
        
        **Built for:** AWS Partners, Customers, and Internal Teams
        
        **Powered by:** Amazon Q AI Assistant
        """)
    
    
    page = st.sidebar.selectbox(
        "Choose Assessment Type",
        ["🏠 Home", "📊 MAP Assessment", "💰 OLA Analysis", "🖥️ ONE OLA (Windows & Storage)", "📈 Results Dashboard"]
    )
    
    # Check if page should be overridden by button clicks
    if 'page' in st.session_state:
        page = st.session_state.page
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "📊 MAP Assessment":
        show_map_assessment()
    elif page == "💰 OLA Analysis":
        show_ola_analysis()
    elif page == "🖥️ ONE OLA (Windows & Storage)":
        show_one_ola()
    elif page == "📈 Results Dashboard":
        show_results_dashboard()
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Amazon Q AWS Programs Toolkit v1.0**")
    with col2:
        st.markdown("Built for MAP, OLA, and ONE OLA programs")
    with col3:
        st.markdown("🤖 Powered by Amazon Q")

def show_home_page():
    st.subheader("Welcome to the AWS Programs Assessment Toolkit")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🚀 MAP Assessment
        **Migration Acceleration Program**
        - Server inventory analysis
        - AWS service recommendations
        - Migration timeline planning
        - Cost estimation & ROI analysis
        
        **Best for:** Complete migration projects
        """)
        if st.button("Start MAP Assessment", key="map_btn"):
            st.session_state.page = "📊 MAP Assessment"
            st.rerun()
    
    with col2:
        st.markdown("""
        ### 💰 OLA Analysis
        **Optimization & Licensing Assessment**
        - **Broad multi-platform** optimization
        - General licensing strategies (all workloads)
        - Portfolio-wide cost optimization
        - Right-sizing across all services
        
        **Best for:** Mixed environments (Windows + Linux)
        """)
        if st.button("Start OLA Analysis", key="ola_btn"):
            st.session_state.page = "💰 OLA Analysis"
            st.rerun()
    
    with col3:
        st.markdown("""
        ### 🖥️ ONE OLA Specialist
        **Windows Server & Storage Deep Dive**
        - **Windows-specific** licensing (Hybrid Benefit)
        - Storage specialization (FSx, EBS, S3)
        - Active Directory integration
        - SQL Server optimization
        
        **Best for:** Windows-heavy environments (70%+ Windows)
        """)
        if st.button("Start ONE OLA", key="one_ola_btn"):
            st.session_state.page = "🖥️ ONE OLA (Windows & Storage)"
            st.rerun()
    
    # Add comparison table
    st.subheader("🔍 Program Comparison")
    comparison_data = {
        'Aspect': [
            'Scope',
            'Focus Area',
            'Licensing Analysis',
            'Storage Analysis',
            'Best For',
            'Typical Savings',
            'Assessment Depth'
        ],
        'OLA (Broad Optimization)': [
            'Multi-platform (Windows + Linux + Containers)',
            'Portfolio-wide cost optimization',
            'General BYOL vs License Included',
            'Basic storage tiering recommendations',
            'Mixed environments, broad optimization',
            '20-35% overall cost reduction',
            'Wide but general analysis'
        ],
        'ONE OLA (Windows & Storage)': [
            'Windows Server and Storage specialization',
            'Deep Windows and storage optimization',
            'Windows Hybrid Benefit, SQL Server licensing',
            'Detailed FSx, EBS, S3 migration strategies',
            'Windows-heavy environments (70%+ Windows)',
            '40-60% on Windows workloads specifically',
            'Deep, specialized analysis'
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    # Recent assessments
    st.subheader("📋 Recent Assessments")
    sample_assessments = pd.DataFrame({
        'Customer': ['Acme Corp', 'TechStart Inc', 'Global Enterprises', 'Financial Corp'],
        'Type': ['MAP', 'OLA', 'ONE OLA', 'OLA'],
        'Status': ['Complete', 'In Progress', 'Complete', 'Complete'],
        'Servers': [127, 45, 89, 234],
        'Windows %': ['65%', '30%', '85%', '45%'],
        'Potential Savings': ['35%', '28%', '52%', '31%'],
        'Date': ['2024-12-15', '2024-12-18', '2024-12-20', '2024-12-22']
    })
    st.dataframe(sample_assessments, use_container_width=True)

def show_map_assessment():
    st.subheader("📊 Migration Acceleration Program (MAP) Assessment")
    
    # Initialize step if not exists
    if 'map_step' not in st.session_state:
        st.session_state.map_step = 0
    
    # Progress indicator
    progress_steps = ["Project Setup", "Data Upload", "Validation", "Analysis", "Results"]
    current_step = st.session_state.map_step
    
    # Debug info (remove in production)
    st.sidebar.write(f"Debug: Current step = {current_step}")
    
    # Progress bar
    progress_cols = st.columns(len(progress_steps))
    for i, (col, step) in enumerate(zip(progress_cols, progress_steps)):
        with col:
            if i <= current_step:
                st.markdown(f"✅ **{step}**")
            else:
                st.markdown(f"⏳ {step}")
    
    st.progress((current_step + 1) / len(progress_steps))
    
    if current_step == 0:
        show_project_setup()
    elif current_step == 1:
        show_data_upload()
    elif current_step == 2:
        show_data_validation()
    elif current_step == 3:
        show_analysis_progress()
    elif current_step == 4:
        show_assessment_results()
    else:
        # Reset if step is invalid
        st.session_state.map_step = 0
        st.rerun()

def show_project_setup():
    st.subheader("Step 1: Project Setup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        customer_name = st.text_input("Customer Name", placeholder="Enter customer name")
        project_type = st.selectbox("Assessment Type", ["MAP - Full Assessment", "MAP - Quick Assessment"])
        region = st.selectbox("Primary AWS Region", ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"])
    
    with col2:
        timeline = st.selectbox("Project Timeline", ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"])
        complexity = st.selectbox("Expected Complexity", ["Low (< 50 servers)", "Medium (50-200 servers)", "High (200+ servers)"])
        
    if st.button("Next: Upload Data", disabled=not customer_name):
        st.session_state.map_step = 1
        st.session_state.project_info = {
            'customer': customer_name,
            'type': project_type,
            'region': region,
            'timeline': timeline,
            'complexity': complexity
        }
        st.rerun()

def show_data_upload():
    st.subheader("Step 2: Data Upload")
    
    st.markdown("### 📁 Upload Your Assessment Data")
    
    # Show expected format
    with st.expander("📋 Expected CSV Format", expanded=False):
        st.markdown("""
        Your CSV file should contain these columns:
        - **Server_Name**: Unique server identifier
        - **CPU_Cores**: Number of CPU cores
        - **Memory_GB**: RAM in gigabytes
        - **Storage_GB**: Storage capacity in gigabytes
        - **OS**: Operating system (e.g., "Windows Server 2019", "Linux Ubuntu 20.04")
        - **Application_Count**: Number of applications (optional)
        - **Storage_Type**: Storage type (e.g., "SSD", "HDD", "SAN") (optional)
        """)
        
        # Sample CSV download
        sample_csv = """Server_Name,CPU_Cores,Memory_GB,Storage_GB,OS,Application_Count,Storage_Type
WebServer01,4,8,500,Windows Server 2019,3,SSD
DBServer01,8,32,2000,Windows Server 2016,1,SAN
AppServer01,2,4,100,Linux Ubuntu 20.04,5,HDD
FileServer01,4,16,1000,Windows Server 2019,2,SSD"""
        
        st.download_button(
            label="📥 Download Sample CSV Template",
            data=sample_csv,
            file_name="server_inventory_template.csv",
            mime="text/csv"
        )
    
    # File upload
    uploaded_file = st.file_uploader(
        "Server Inventory (CSV)",
        type=['csv'],
        help="Upload CSV with your server inventory data"
    )
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ File uploaded successfully! Found {len(df)} servers.")
            
            # Preview data
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            # Store data in session
            st.session_state.server_data = df
            
            if st.button("Next: Validate Data"):
                st.session_state.map_step = 2
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.markdown("**Common issues:**")
            st.markdown("- Check that your file is in CSV format")
            st.markdown("- Ensure column names match the expected format")
            st.markdown("- Verify there are no special characters in the data")
    
    # Sample data option
    st.markdown("### 📊 Or Use Sample Data for Testing")
    st.info("👆 Perfect for trying out the app without uploading your own data")
    if st.button("Load Sample Data"):
        sample_data = create_sample_data()
        st.session_state.server_data = sample_data
        st.session_state.map_step = 2
        st.rerun()

def show_data_validation():
    st.subheader("Step 3: Data Validation")
    
    if 'server_data' in st.session_state:
        df = st.session_state.server_data
        
        # Validation metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Servers", len(df))
        with col2:
            windows_count = len(df[df['OS'].str.contains('Windows', na=False, case=False)])
            st.metric("Windows Servers", windows_count)
        with col3:
            linux_count = len(df[df['OS'].str.contains('Linux', na=False, case=False)])
            st.metric("Linux Servers", linux_count)
        with col4:
            missing_data = df.isnull().sum().sum()
            st.metric("Missing Data Points", missing_data)
        
        # Data quality issues
        st.subheader("🔍 Data Quality Analysis")
        
        issues = []
        if df['CPU_Cores'].isnull().any():
            issues.append(f"• {df['CPU_Cores'].isnull().sum()} servers missing CPU information")
        if df['Memory_GB'].isnull().any():
            issues.append(f"• {df['Memory_GB'].isnull().sum()} servers missing memory information")
        if df['Storage_GB'].isnull().any():
            issues.append(f"• {df['Storage_GB'].isnull().sum()} servers missing storage information")
        
        if issues:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown("⚠️ **Data Quality Issues Found:**")
            for issue in issues:
                st.markdown(issue)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("✅ **Data quality looks good! No issues found.**")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Visualization
        fig = px.histogram(df, x='OS', title="Server Distribution by Operating System")
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous Step"):
                st.session_state.map_step = 1
                st.rerun()
        with col2:
            if st.button("Next: Run Analysis →"):
                st.session_state.map_step = 3
                st.rerun()

def show_analysis_progress():
    st.subheader("Step 4: Running Analysis")
    
    # Simulate analysis progress
    if 'analysis_progress' not in st.session_state:
        st.session_state.analysis_progress = 0
    
    progress_bar = st.progress(st.session_state.analysis_progress)
    status_text = st.empty()
    
    analysis_steps = [
        "Analyzing server inventory...",
        "Mapping to AWS services...",
        "Calculating cost estimates...",
        "Generating recommendations...",
        "Creating reports..."
    ]
    
    if st.session_state.analysis_progress < 100:
        current_step_idx = min(int(st.session_state.analysis_progress / 20), len(analysis_steps) - 1)
        status_text.text(analysis_steps[current_step_idx])
        
        # Auto-increment progress (in real app, this would be actual analysis)
        if st.button("Continue Analysis"):
            st.session_state.analysis_progress = min(100, st.session_state.analysis_progress + 20)
            st.rerun()
    else:
        status_text.text("✅ Analysis complete!")
        if st.button("View Results →"):
            st.session_state.map_step = 4
            st.rerun()

def show_assessment_results():
    st.subheader("Step 5: Assessment Results")
    
    if 'server_data' in st.session_state:
        df = st.session_state.server_data
        
        # Executive summary
        st.subheader("📊 Executive Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Servers", len(df))
        with col2:
            st.metric("Est. Monthly Cost", "$12,450", delta="-35%")
        with col3:
            st.metric("Migration Ready", "89%", delta="Good")
        with col4:
            st.metric("Timeline", "8-12 months")
        
        # Key recommendations
        st.subheader("🎯 Key Recommendations")
        recommendations = [
            "Right-size 23 over-provisioned servers → Save $2,100/month",
            "Apply Hybrid Benefit to Windows servers → Save 40%",
            "Migrate file servers to Amazon FSx → Save $1,800/month",
            "Convert dev/test servers to Spot Instances → Save 70%"
        ]
        
        for rec in recommendations:
            st.markdown(f"• {rec}")
        
        # Charts
        st.subheader("📈 Analysis Charts")
        
        tab1, tab2, tab3 = st.tabs(["Cost Analysis", "Server Distribution", "Migration Timeline"])
        
        with tab1:
            # Cost comparison chart
            cost_data = pd.DataFrame({
                'Category': ['Current On-Premises', 'AWS (No Optimization)', 'AWS (Optimized)'],
                'Monthly Cost': [18000, 15000, 12450]
            })
            fig = px.bar(cost_data, x='Category', y='Monthly Cost', 
                        title="Cost Comparison Analysis")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Server distribution
            fig = px.pie(df, names='OS', title="Server Distribution by OS")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Migration timeline
            timeline_data = pd.DataFrame({
                'Phase': ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'],
                'Duration': [2, 3, 4, 3],
                'Servers': [32, 45, 35, 15]
            })
            fig = px.bar(timeline_data, x='Phase', y=['Duration', 'Servers'],
                        title="Migration Timeline and Server Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        # Amazon Q integration
        st.subheader("🤖 Ask Amazon Q")
        user_question = st.text_input("Ask about these results...", 
                                    placeholder="e.g., How can I reduce costs further?")
        
        if user_question:
            # Simulate Amazon Q response
            q_responses = {
                "cost": "Based on your assessment, you can achieve additional savings by: 1) Implementing auto-scaling for variable workloads, 2) Using S3 Intelligent Tiering for storage, 3) Considering Aurora Serverless for databases with unpredictable usage patterns.",
                "timeline": "Your migration timeline can be optimized by: 1) Starting with stateless applications first, 2) Running pilot migrations in parallel, 3) Using AWS Application Migration Service for faster server migrations.",
                "default": "I can help you customize this analysis further. Would you like me to focus on specific areas like security, compliance, or performance optimization?"
            }
            
            response_key = "default"
            if "cost" in user_question.lower():
                response_key = "cost"
            elif "timeline" in user_question.lower():
                response_key = "timeline"
            
            st.markdown(f"**Amazon Q:** {q_responses[response_key]}")
        
        # Export options
        st.subheader("📄 Export Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Executive Report"):
                st.success("Executive report generated! (Download would start here)")
        with col2:
            if st.button("📋 Technical Details"):
                st.success("Technical report generated! (Download would start here)")
        with col3:
            if st.button("💰 Cost Model"):
                st.success("Cost model exported! (Download would start here)")

def show_ola_analysis():
    st.subheader("💰 Optimization and Licensing Assessment (OLA)")
    st.info("🎯 **Focus:** Broad, multi-platform optimization across your entire AWS environment")
    
    # Progress indicator
    progress_steps = ["Environment Setup", "Multi-Platform Analysis", "Cost Optimization", "Licensing Review", "Portfolio Results"]
    current_step = st.session_state.get('ola_step', 0)
    
    # Progress bar
    progress_cols = st.columns(len(progress_steps))
    for i, (col, step) in enumerate(zip(progress_cols, progress_steps)):
        with col:
            if i <= current_step:
                st.markdown(f"✅ **{step}**")
            else:
                st.markdown(f"⏳ {step}")
    
    st.progress((current_step + 1) / len(progress_steps))
    
    if current_step == 0:
        show_ola_environment_setup()
    elif current_step == 1:
        show_ola_multiplatform_analysis()
    elif current_step == 2:
        show_ola_cost_optimization()
    elif current_step == 3:
        show_ola_licensing_review()
    elif current_step == 4:
        show_ola_portfolio_results()

def show_ola_environment_setup():
    st.subheader("Step 1: Environment Setup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏢 Environment Profile")
        customer_name = st.text_input("Customer Name", placeholder="Enter customer name")
        environment_type = st.selectbox("Environment Type", [
            "Mixed (Windows + Linux + Containers)",
            "Primarily Linux with some Windows",
            "Primarily Windows with some Linux",
            "Multi-cloud (AWS + On-premises)"
        ])
        workload_types = st.multiselect("Primary Workload Types", [
            "Web Applications",
            "Databases",
            "File Servers",
            "Development/Test",
            "Analytics/Big Data",
            "Containerized Applications",
            "Legacy Applications"
        ])
    
    with col2:
        st.markdown("### 🎯 Optimization Goals")
        optimization_focus = st.multiselect("Optimization Priorities", [
            "Cost Reduction",
            "Performance Improvement",
            "License Optimization",
            "Right-sizing",
            "Reserved Instance Planning",
            "Storage Optimization",
            "Security Enhancement"
        ])
        timeline = st.selectbox("Optimization Timeline", ["Immediate (0-3 months)", "Short-term (3-6 months)", "Long-term (6-12 months)"])
        budget_constraint = st.selectbox("Budget Approach", ["Minimize costs", "Balance cost and performance", "Performance first"])
    
    if st.button("Next: Multi-Platform Analysis", disabled=not customer_name):
        st.session_state.ola_step = 1
        st.session_state.ola_profile = {
            'customer': customer_name,
            'environment_type': environment_type,
            'workload_types': workload_types,
            'optimization_focus': optimization_focus,
            'timeline': timeline,
            'budget_constraint': budget_constraint
        }
        st.rerun()

def show_ola_multiplatform_analysis():
    st.subheader("Step 2: Multi-Platform Analysis")
    
    # Upload multiple data sources
    st.markdown("### 📊 Upload Your Environment Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Server Inventory (Required)**")
        server_file = st.file_uploader("Server Inventory CSV", type=['csv'], key="ola_servers")
        
        st.markdown("**AWS Cost Data (Optional)**")
        cost_file = st.file_uploader("AWS Cost & Usage Report", type=['csv'], key="ola_costs")
    
    with col2:
        st.markdown("**License Inventory (Optional)**")
        license_file = st.file_uploader("License Inventory", type=['csv', 'xlsx'], key="ola_licenses")
        
        st.markdown("**Performance Data (Optional)**")
        perf_file = st.file_uploader("Performance Metrics", type=['json', 'csv'], key="ola_perf")
    
    # Sample data option
    if st.button("Use Sample Multi-Platform Data"):
        sample_data = create_multiplatform_sample_data()
        st.session_state.ola_data = sample_data
        st.success("✅ Sample multi-platform data loaded!")
        
        # Show data preview
        st.subheader("📋 Environment Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Servers", len(sample_data))
        with col2:
            windows_count = len(sample_data[sample_data['OS'].str.contains('Windows', na=False, case=False)])
            st.metric("Windows Servers", windows_count)
        with col3:
            linux_count = len(sample_data[sample_data['OS'].str.contains('Linux', na=False, case=False)])
            st.metric("Linux Servers", linux_count)
        with col4:
            container_count = len(sample_data[sample_data['Workload_Type'].str.contains('Container', na=False, case=False)])
            st.metric("Containerized", container_count)
        
        # Platform distribution chart
        platform_dist = sample_data['Platform_Category'].value_counts()
        fig = px.pie(values=platform_dist.values, names=platform_dist.index, 
                    title="Platform Distribution")
        st.plotly_chart(fig, use_container_width=True)
        
        if st.button("Next: Cost Optimization Analysis"):
            st.session_state.ola_step = 2
            st.rerun()

def show_ola_cost_optimization():
    st.subheader("Step 3: Cost Optimization Analysis")
    
    if 'ola_data' in st.session_state:
        df = st.session_state.ola_data
        
        st.markdown("### 💰 Portfolio-Wide Cost Analysis")
        
        # Cost optimization opportunities
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Right-Sizing Opportunities")
            rightsizing_data = pd.DataFrame({
                'Category': ['Over-provisioned', 'Under-provisioned', 'Optimally sized'],
                'Count': [23, 8, 19],
                'Potential Savings': ['$2,100/month', '$0', '$0']
            })
            st.dataframe(rightsizing_data, hide_index=True)
            
            # Right-sizing chart
            fig = px.bar(rightsizing_data, x='Category', y='Count', 
                        title="Right-sizing Analysis")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🏷️ Reserved Instance Opportunities")
            ri_data = pd.DataFrame({
                'Instance Family': ['m5', 't3', 'r5', 'c5'],
                'Current On-Demand': [12, 8, 6, 4],
                'RI Recommendation': ['1-year Partial', '1-year All Upfront', '3-year Partial', '1-year Partial'],
                'Monthly Savings': ['$450', '$180', '$320', '$120']
            })
            st.dataframe(ri_data, hide_index=True)
            
            # RI savings chart
            fig = px.bar(ri_data, x='Instance Family', y='Current On-Demand', 
                        title="Reserved Instance Candidates")
            st.plotly_chart(fig, use_container_width=True)
        
        # Storage optimization
        st.markdown("#### 💾 Storage Optimization")
        storage_data = pd.DataFrame({
            'Storage Type': ['EBS gp2', 'EBS io1', 'S3 Standard', 'EFS'],
            'Current Usage (GB)': [2500, 500, 10000, 1500],
            'Recommended': ['Upgrade to gp3', 'Consider gp3', 'Add Intelligent Tiering', 'Optimize access patterns'],
            'Monthly Savings': ['$125', '$200', '$300', '$75']
        })
        st.dataframe(storage_data, use_container_width=True, hide_index=True)
        
        if st.button("Next: Licensing Review"):
            st.session_state.ola_step = 3
            st.rerun()

def show_ola_licensing_review():
    st.subheader("Step 4: Multi-Platform Licensing Review")
    
    st.markdown("### 📋 License Optimization Across All Platforms")
    
    tab1, tab2, tab3 = st.tabs(["Windows Licensing", "Database Licensing", "Other Software"])
    
    with tab1:
        st.markdown("#### 🖥️ Windows Server Licensing")
        windows_license_data = pd.DataFrame({
            'License Type': ['Windows Server Standard', 'Windows Server Datacenter', 'SQL Server Standard', 'SQL Server Enterprise'],
            'Current Count': [45, 12, 8, 3],
            'Hybrid Benefit Eligible': [45, 12, 8, 3],
            'Monthly Savings': ['$1,800', '$960', '$640', '$450']
        })
        st.dataframe(windows_license_data, hide_index=True)
        
        total_windows_savings = 1800 + 960 + 640 + 450
        st.success(f"💰 **Total Windows Hybrid Benefit Savings: ${total_windows_savings:,}/month**")
    
    with tab2:
        st.markdown("#### 🗄️ Database Licensing")
        db_license_data = pd.DataFrame({
            'Database': ['Oracle Enterprise', 'SQL Server Enterprise', 'MySQL Enterprise', 'PostgreSQL'],
            'Current Model': ['BYOL on EC2', 'BYOL on EC2', 'License Included', 'Open Source'],
            'Recommendation': ['Consider RDS Oracle', 'Consider RDS SQL Server', 'Optimize instance size', 'Consider Aurora'],
            'Impact': ['Reduce management overhead', 'Potential cost savings', 'Right-size instances', 'Better performance']
        })
        st.dataframe(db_license_data, hide_index=True)
    
    with tab3:
        st.markdown("#### 🛠️ Other Software Licensing")
        other_license_data = pd.DataFrame({
            'Software': ['Red Hat Enterprise Linux', 'SUSE Linux', 'VMware vSphere', 'Backup Software'],
            'Current Approach': ['BYOL', 'BYOL', 'On-premises', 'Third-party'],
            'AWS Alternative': ['RHEL on AWS', 'SLES on AWS', 'Native AWS services', 'AWS Backup'],
            'Consideration': ['Compare costs', 'Evaluate support', 'Migration complexity', 'Feature comparison']
        })
        st.dataframe(other_license_data, hide_index=True)
    
    if st.button("Next: Portfolio Results"):
        st.session_state.ola_step = 4
        st.rerun()

def show_ola_portfolio_results():
    st.subheader("Step 5: Portfolio Optimization Results")
    
    st.markdown("### 📊 Executive Summary - Portfolio-Wide Optimization")
    
    # Executive metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Servers Analyzed", "127", delta="Mixed environment")
    with col2:
        st.metric("Monthly Cost Reduction", "$4,850", delta="-32%")
    with col3:
        st.metric("Annual Savings Potential", "$58,200", delta="ROI: 340%")
    with col4:
        st.metric("Implementation Timeline", "3-6 months", delta="Phased approach")
    
    # Detailed recommendations
    st.markdown("### 🎯 Top Optimization Recommendations")
    
    recommendations = [
        {"Priority": "High", "Action": "Apply Windows Hybrid Benefit", "Impact": "$3,850/month", "Effort": "Low", "Timeline": "Immediate"},
        {"Priority": "High", "Action": "Right-size over-provisioned instances", "Impact": "$2,100/month", "Effort": "Medium", "Timeline": "1-2 months"},
        {"Priority": "Medium", "Action": "Purchase Reserved Instances", "Impact": "$1,070/month", "Effort": "Low", "Timeline": "Immediate"},
        {"Priority": "Medium", "Action": "Optimize storage tiers", "Impact": "$700/month", "Effort": "Medium", "Timeline": "2-3 months"},
        {"Priority": "Low", "Action": "Migrate to managed databases", "Impact": "$500/month", "Effort": "High", "Timeline": "3-6 months"}
    ]
    
    recommendations_df = pd.DataFrame(recommendations)
    st.dataframe(recommendations_df, use_container_width=True, hide_index=True)
    
    # Charts
    st.markdown("### 📈 Portfolio Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Cost Breakdown", "Platform Distribution", "Optimization Timeline"])
    
    with tab1:
        # Cost breakdown
        cost_data = pd.DataFrame({
            'Category': ['Compute', 'Storage', 'Database', 'Networking', 'Other'],
            'Current Monthly Cost': [8500, 2200, 3100, 800, 1200],
            'Optimized Monthly Cost': [6200, 1800, 2600, 800, 1000]
        })
        
        fig = px.bar(cost_data, x='Category', y=['Current Monthly Cost', 'Optimized Monthly Cost'],
                    title="Cost Optimization by Category", barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Platform distribution with optimization potential
        platform_data = pd.DataFrame({
            'Platform': ['Windows Server', 'Linux', 'Containers', 'Databases', 'Storage'],
            'Current Servers': [57, 45, 15, 8, 2],
            'Optimization Potential': ['High', 'Medium', 'Low', 'High', 'Medium']
        })
        
        fig = px.scatter(platform_data, x='Platform', y='Current Servers', 
                        color='Optimization Potential', size='Current Servers',
                        title="Platform Distribution and Optimization Potential")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Implementation timeline
        timeline_data = pd.DataFrame({
            'Phase': ['Phase 1 (0-1 month)', 'Phase 2 (1-3 months)', 'Phase 3 (3-6 months)'],
            'Actions': [
                'Hybrid Benefit, Reserved Instances',
                'Right-sizing, Storage optimization',
                'Database migration, Advanced optimization'
            ],
            'Monthly Savings': [4920, 2800, 500],
            'Cumulative Savings': [4920, 7720, 8220]
        })
        
        fig = px.line(timeline_data, x='Phase', y='Cumulative Savings',
                     title="Cumulative Savings Timeline", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # Amazon Q integration
    st.markdown("### 🤖 Ask Amazon Q About Your Portfolio")
    user_question = st.text_input("Ask about your optimization results...", 
                                placeholder="e.g., How can I prioritize these recommendations?")
    
    if user_question:
        ola_responses = {
            "prioritize": "For your mixed environment, I recommend this priority order: 1) Apply Windows Hybrid Benefit immediately (highest ROI, lowest effort), 2) Right-size over-provisioned instances (quick wins), 3) Purchase Reserved Instances for stable workloads, 4) Optimize storage tiers, 5) Consider managed database services for long-term benefits.",
            "timeline": "Your optimization can be implemented in 3 phases: Phase 1 (0-1 month): Licensing and RI changes for immediate $4,920/month savings. Phase 2 (1-3 months): Right-sizing and storage optimization. Phase 3 (3-6 months): Database migrations and advanced optimizations.",
            "risk": "The recommendations are low-risk: Hybrid Benefit and RI purchases have no technical risk. Right-sizing should be done gradually with monitoring. Storage optimization can be tested with non-critical data first.",
            "default": "Your portfolio shows excellent optimization potential with 32% cost reduction possible. The mixed Windows/Linux environment benefits most from licensing optimization and right-sizing. Would you like me to focus on any specific platform or optimization area?"
        }
        
        response_key = "default"
        if "prioritize" in user_question.lower() or "priority" in user_question.lower():
            response_key = "prioritize"
        elif "timeline" in user_question.lower() or "when" in user_question.lower():
            response_key = "timeline"
        elif "risk" in user_question.lower() or "safe" in user_question.lower():
            response_key = "risk"
        
        st.markdown(f"**Amazon Q:** {ola_responses[response_key]}")
    
    # Export options
    st.markdown("### 📄 Export Portfolio Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Executive Summary"):
            st.success("Portfolio executive summary generated!")
    with col2:
        if st.button("📋 Detailed Analysis"):
            st.success("Detailed optimization report generated!")
    with col3:
        if st.button("💰 Business Case"):
            st.success("ROI and business case exported!")

def create_multiplatform_sample_data():
    """Create sample data for OLA multi-platform analysis"""
    import random
    
    platforms = [
        ("Windows Server 2019", "Windows"),
        ("Windows Server 2016", "Windows"), 
        ("Linux Ubuntu 20.04", "Linux"),
        ("Linux CentOS 7", "Linux"),
        ("Linux RHEL 8", "Linux"),
        ("Container (Docker)", "Container")
    ]
    
    workload_types = ["Web Server", "Database", "File Server", "Application Server", "Development", "Container App"]
    
    data = []
    for i in range(1, 101):  # 100 servers for OLA
        platform, category = random.choice(platforms)
        data.append({
            'Server_Name': f"Server{i:03d}",
            'CPU_Cores': random.choice([2, 4, 8, 16, 32]),
            'Memory_GB': random.choice([8, 16, 32, 64, 128]),
            'Storage_GB': random.choice([100, 500, 1000, 2000, 4000]),
            'OS': platform,
            'Platform_Category': category,
            'Workload_Type': random.choice(workload_types),
            'Environment': random.choice(['Production', 'Development', 'Test', 'Staging']),
            'Utilization_CPU': random.randint(10, 90),
            'Monthly_Cost': random.randint(50, 500)
        })
    
    return pd.DataFrame(data)

def show_one_ola():
    st.subheader("🖥️ ONE OLA - Windows Server & Storage Specialization")
    st.info("🎯 **Focus:** Deep specialization in Windows Server environments and storage optimization")
    
    # Progress indicator
    progress_steps = ["Windows Assessment", "Storage Analysis", "AD Integration", "Licensing Deep Dive", "Specialized Results"]
    current_step = st.session_state.get('one_ola_step', 0)
    
    # Progress bar
    progress_cols = st.columns(len(progress_steps))
    for i, (col, step) in enumerate(zip(progress_cols, progress_steps)):
        with col:
            if i <= current_step:
                st.markdown(f"✅ **{step}**")
            else:
                st.markdown(f"⏳ {step}")
    
    st.progress((current_step + 1) / len(progress_steps))
    
    if current_step == 0:
        show_one_ola_windows_assessment()
    elif current_step == 1:
        show_one_ola_storage_analysis()
    elif current_step == 2:
        show_one_ola_ad_integration()
    elif current_step == 3:
        show_one_ola_licensing_deep_dive()
    elif current_step == 4:
        show_one_ola_specialized_results()

def show_one_ola_windows_assessment():
    st.subheader("Step 1: Windows Environment Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🖥️ Windows Infrastructure Profile")
        customer_name = st.text_input("Customer Name", placeholder="Enter customer name")
        windows_percentage = st.slider("Windows Server Percentage", 0, 100, 85, 5)
        
        windows_versions = st.multiselect("Windows Server Versions", [
            "Windows Server 2012 R2 (End of Support)",
            "Windows Server 2016",
            "Windows Server 2019", 
            "Windows Server 2022"
        ], default=["Windows Server 2016", "Windows Server 2019"])
        
        ad_environment = st.selectbox("Active Directory Environment", [
            "Single domain, single forest",
            "Multiple domains, single forest",
            "Multiple forests",
            "Hybrid (on-premises + cloud)",
            "No Active Directory"
        ])
    
    with col2:
        st.markdown("### 💾 Storage Infrastructure")
        storage_types = st.multiselect("Current Storage Types", [
            "File Servers (SMB/CIFS)",
            "DFS (Distributed File System)",
            "SAN/NAS Storage",
            "Local Server Storage",
            "Backup/Archive Storage"
        ])
        
        file_server_count = st.number_input("Number of File Servers", 0, 100, 15)
        total_storage_tb = st.number_input("Total Storage (TB)", 0, 1000, 50)
        
        sql_server = st.checkbox("SQL Server Environment")
        if sql_server:
            sql_versions = st.multiselect("SQL Server Versions", [
                "SQL Server 2012",
                "SQL Server 2014", 
                "SQL Server 2016",
                "SQL Server 2017",
                "SQL Server 2019",
                "SQL Server 2022"
            ])
    
    # Windows specialization indicators
    st.markdown("### 🎯 Windows Specialization Indicators")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if windows_percentage >= 70:
            st.success(f"✅ {windows_percentage}% Windows - Perfect for ONE OLA")
        else:
            st.warning(f"⚠️ {windows_percentage}% Windows - Consider regular OLA")
    
    with col2:
        if file_server_count > 5:
            st.success(f"✅ {file_server_count} File Servers - Storage specialization beneficial")
        else:
            st.info(f"ℹ️ {file_server_count} File Servers - Limited storage focus")
    
    with col3:
        if sql_server:
            st.success("✅ SQL Server - Licensing optimization opportunities")
        else:
            st.info("ℹ️ No SQL Server - Focus on Windows Server licensing")
    
    if st.button("Next: Storage Analysis", disabled=not customer_name):
        st.session_state.one_ola_step = 1
        st.session_state.one_ola_profile = {
            'customer': customer_name,
            'windows_percentage': windows_percentage,
            'windows_versions': windows_versions,
            'ad_environment': ad_environment,
            'storage_types': storage_types,
            'file_server_count': file_server_count,
            'total_storage_tb': total_storage_tb,
            'sql_server': sql_server
        }
        st.rerun()

def show_one_ola_storage_analysis():
    st.subheader("Step 2: Storage Specialization Analysis")
    
    st.markdown("### 💾 Detailed Storage Assessment")
    
    # File server analysis
    st.markdown("#### 📁 File Server Analysis")
    
    if st.button("Load Windows Storage Sample Data"):
        storage_data = create_windows_storage_sample_data()
        st.session_state.one_ola_storage = storage_data
        
        # Display storage analysis
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("File Servers", len(storage_data))
        with col2:
            total_capacity = storage_data['Capacity_GB'].sum()
            st.metric("Total Capacity", f"{total_capacity:,} GB")
        with col3:
            total_used = storage_data['Used_GB'].sum()
            st.metric("Used Storage", f"{total_used:,} GB")
        with col4:
            avg_utilization = (total_used / total_capacity * 100)
            st.metric("Avg Utilization", f"{avg_utilization:.1f}%")
        
        # Storage recommendations
        st.markdown("#### 🎯 FSx for Windows File Server Recommendations")
        
        fsx_recommendations = []
        for _, server in storage_data.iterrows():
            if server['Access_Pattern'] == 'High':
                fsx_type = "Multi-AZ"
                throughput = "512 MB/s"
            elif server['Access_Pattern'] == 'Medium':
                fsx_type = "Single-AZ"
                throughput = "64 MB/s"
            else:
                fsx_type = "Single-AZ"
                throughput = "16 MB/s"
            
            monthly_cost = server['Used_GB'] * 0.13  # FSx pricing estimate
            
            fsx_recommendations.append({
                'File Server': server['Server_Name'],
                'Current Storage (GB)': server['Used_GB'],
                'Recommended FSx': fsx_type,
                'Throughput': throughput,
                'Est. Monthly Cost': f"${monthly_cost:.0f}",
                'Migration Strategy': 'AWS DataSync + Cutover'
            })
        
        fsx_df = pd.DataFrame(fsx_recommendations)
        st.dataframe(fsx_df, use_container_width=True, hide_index=True)
        
        # Storage tiering analysis
        st.markdown("#### 📊 Storage Tiering Opportunities")
        
        tiering_data = pd.DataFrame({
            'Data Type': ['Frequently Accessed', 'Infrequently Accessed', 'Archive/Backup', 'Temp/Cache'],
            'Current Location': ['File Servers', 'File Servers', 'Tape/Local', 'Local Disk'],
            'AWS Recommendation': ['FSx for Windows', 'S3 Intelligent Tiering', 'S3 Glacier Deep Archive', 'Instance Store/EBS'],
            'Monthly Cost Reduction': ['$0 (performance gain)', '$450', '$1,200', '$150']
        })
        
        st.dataframe(tiering_data, use_container_width=True, hide_index=True)
        
        # Storage migration timeline
        fig = px.timeline(
            pd.DataFrame({
                'Task': ['Phase 1: Critical File Servers', 'Phase 2: Department Shares', 'Phase 3: Archive Data'],
                'Start': ['2025-01-01', '2025-02-01', '2025-03-01'],
                'Finish': ['2025-01-31', '2025-02-28', '2025-04-30'],
                'Resource': ['FSx Multi-AZ', 'FSx Single-AZ', 'S3 Glacier']
            }),
            x_start="Start", x_end="Finish", y="Task", color="Resource",
            title="Storage Migration Timeline"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        if st.button("Next: Active Directory Integration"):
            st.session_state.one_ola_step = 2
            st.rerun()

def show_one_ola_ad_integration():
    st.subheader("Step 3: Active Directory Integration Planning")
    
    st.markdown("### 🔐 Active Directory Architecture Analysis")
    
    # AD integration options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏢 Current AD Environment")
        current_ad = st.session_state.get('one_ola_profile', {}).get('ad_environment', 'Single domain')
        st.info(f"**Current Setup:** {current_ad}")
        
        ad_metrics = pd.DataFrame({
            'Metric': ['Domain Controllers', 'User Accounts', 'Computer Accounts', 'Group Policies'],
            'Count': [4, 1250, 890, 45],
            'Complexity': ['Medium', 'High', 'High', 'Medium']
        })
        st.dataframe(ad_metrics, hide_index=True)
    
    with col2:
        st.markdown("#### ☁️ AWS AD Integration Options")
        
        ad_options = pd.DataFrame({
            'Option': ['AWS Managed Microsoft AD', 'AD Connector', 'Simple AD'],
            'Best For': ['New AWS workloads', 'Hybrid scenarios', 'Basic needs only'],
            'Cost/Month': ['$146', '$36', '$36'],
            'Features': ['Full AD features', 'Proxy to on-premises', 'Basic LDAP'],
            'Recommendation': ['✅ Recommended', '⚠️ Consider', '❌ Not suitable']
        })
        st.dataframe(ad_options, hide_index=True)
    
    # AD integration architecture
    st.markdown("#### 🏗️ Recommended AD Architecture")
    
    architecture_choice = st.radio(
        "Select AD Integration Approach:",
        [
            "AWS Managed Microsoft AD (Standalone)",
            "AWS Managed Microsoft AD (Trust with on-premises)",
            "AD Connector (Hybrid)",
            "Migrate existing AD to AWS"
        ]
    )
    
    if architecture_choice == "AWS Managed Microsoft AD (Standalone)":
        st.success("✅ **Recommended for ONE OLA customers**")
        st.markdown("""
        **Benefits:**
        - Full Microsoft AD features in AWS
        - Seamless integration with FSx for Windows
        - Built-in high availability
        - Managed patching and maintenance
        
        **Implementation:**
        - Create new AWS Managed Microsoft AD
        - Migrate user accounts and groups
        - Establish trust relationships if needed
        - Configure FSx to use AWS Managed AD
        """)
    
    # FSx AD integration
    st.markdown("#### 🔗 FSx Active Directory Integration")
    
    fsx_ad_config = pd.DataFrame({
        'FSx File System': ['Finance-FS', 'HR-FS', 'Engineering-FS', 'Archive-FS'],
        'AD Domain': ['corp.company.com', 'corp.company.com', 'corp.company.com', 'corp.company.com'],
        'Access Control': ['Finance Group', 'HR Group', 'Engineering Group', 'All Users (Read)'],
        'Backup Policy': ['Daily', 'Daily', 'Hourly', 'Weekly']
    })
    st.dataframe(fsx_ad_config, use_container_width=True, hide_index=True)
    
    if st.button("Next: Licensing Deep Dive"):
        st.session_state.one_ola_step = 3
        st.rerun()

def show_one_ola_licensing_deep_dive():
    st.subheader("Step 4: Windows Licensing Deep Dive")
    
    st.markdown("### 💰 Specialized Windows Licensing Analysis")
    
    # Windows Server licensing
    st.markdown("#### 🖥️ Windows Server Hybrid Benefit Analysis")
    
    windows_licensing = pd.DataFrame({
        'Server Type': ['Domain Controllers', 'File Servers', 'Application Servers', 'Database Servers', 'Web Servers'],
        'Count': [4, 15, 25, 8, 12],
        'Current Edition': ['Standard', 'Standard', 'Standard', 'Datacenter', 'Standard'],
        'Cores per Server': [8, 4, 8, 16, 4],
        'Hybrid Benefit Eligible': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        'Monthly Savings': ['$320', '$600', '$1,000', '$1,280', '$480']
    })
    
    st.dataframe(windows_licensing, use_container_width=True, hide_index=True)
    
    total_windows_savings = 320 + 600 + 1000 + 1280 + 480
    st.success(f"💰 **Total Windows Server Hybrid Benefit Savings: ${total_windows_savings:,}/month**")
    
    # SQL Server licensing (if applicable)
    if st.session_state.get('one_ola_profile', {}).get('sql_server'):
        st.markdown("#### 🗄️ SQL Server Licensing Optimization")
        
        sql_licensing = pd.DataFrame({
            'SQL Instance': ['PROD-SQL01', 'PROD-SQL02', 'DEV-SQL01', 'TEST-SQL01'],
            'Current Edition': ['Enterprise', 'Standard', 'Standard', 'Developer'],
            'Cores': [16, 8, 4, 4],
            'Current Model': ['BYOL on EC2', 'BYOL on EC2', 'BYOL on EC2', 'BYOL on EC2'],
            'Recommendation': ['RDS SQL Enterprise', 'RDS SQL Standard', 'RDS SQL Standard', 'RDS SQL Express'],
            'Monthly Impact': ['-$500 (managed)', '+$200 (license)', 'Break-even', '-$100 (downgrade)']
        })
        
        st.dataframe(sql_licensing, use_container_width=True, hide_index=True)
        
        st.info("💡 **SQL Server Strategy:** Mix of RDS managed services and EC2 with Hybrid Benefit based on workload requirements")
    
    # Licensing compliance and optimization
    st.markdown("#### 📋 Licensing Compliance & Optimization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Current Licensing Posture**")
        compliance_data = pd.DataFrame({
            'License Type': ['Windows Server', 'SQL Server', 'Office/M365', 'Other Microsoft'],
            'Compliance Status': ['✅ Compliant', '⚠️ Review needed', '✅ Compliant', '✅ Compliant'],
            'Optimization Potential': ['High', 'Medium', 'Low', 'Low']
        })
        st.dataframe(compliance_data, hide_index=True)
    
    with col2:
        st.markdown("**Optimization Strategies**")
        strategies = [
            "Apply Hybrid Benefit to all eligible Windows workloads",
            "Consolidate SQL Server instances where possible",
            "Use RDS for managed SQL Server workloads",
            "Implement license tracking and monitoring",
            "Regular license optimization reviews"
        ]
        for strategy in strategies:
            st.markdown(f"• {strategy}")
    
    # License cost modeling
    st.markdown("#### 📊 License Cost Modeling")
    
    cost_model = pd.DataFrame({
        'Scenario': ['Current (On-premises)', 'Lift & Shift (No Hybrid Benefit)', 'Optimized (With Hybrid Benefit)', 'Fully Managed (RDS + Hybrid Benefit)'],
        'Monthly License Cost': ['$8,500', '$8,500', '$4,820', '$5,200'],
        'Monthly Infrastructure': ['$2,000', '$6,200', '$6,200', '$5,800'],
        'Total Monthly Cost': ['$10,500', '$14,700', '$11,020', '$11,000'],
        'vs Current': ['Baseline', '+40%', '+5%', '+5%']
    })
    
    st.dataframe(cost_model, use_container_width=True, hide_index=True)
    
    fig = px.bar(cost_model, x='Scenario', y=['Monthly License Cost', 'Monthly Infrastructure'],
                title="License Cost Modeling Scenarios")
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("Next: Specialized Results"):
        st.session_state.one_ola_step = 4
        st.rerun()

def show_one_ola_specialized_results():
    st.subheader("Step 5: Windows & Storage Specialization Results")
    
    st.markdown("### 🎯 ONE OLA Specialized Recommendations")
    
    # Executive summary for Windows specialization
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Windows Servers", "64", delta="85% of environment")
    with col2:
        st.metric("Storage Optimization", "$1,800/month", delta="File server consolidation")
    with col3:
        st.metric("Licensing Savings", "$3,680/month", delta="Hybrid Benefit")
    with col4:
        st.metric("Total Specialized Savings", "$5,480/month", delta="52% reduction")
    
    # Specialized recommendations
    st.markdown("### 🏆 Top Windows & Storage Recommendations")
    
    specialized_recs = [
        {
            "Priority": "Critical",
            "Category": "Windows Licensing",
            "Recommendation": "Apply Windows Server Hybrid Benefit to all 64 servers",
            "Monthly Impact": "$3,680",
            "Implementation": "Immediate - configuration change only",
            "Risk": "None"
        },
        {
            "Priority": "High", 
            "Category": "Storage Consolidation",
            "Recommendation": "Migrate 15 file servers to Amazon FSx for Windows",
            "Monthly Impact": "$1,800",
            "Implementation": "2-3 months with AWS DataSync",
            "Risk": "Low - phased migration"
        },
        {
            "Priority": "High",
            "Category": "Active Directory",
            "Recommendation": "Deploy AWS Managed Microsoft AD with trust relationship",
            "Monthly Impact": "$200 cost, operational benefits",
            "Implementation": "1 month setup + integration",
            "Risk": "Medium - requires AD expertise"
        },
        {
            "Priority": "Medium",
            "Category": "SQL Server",
            "Recommendation": "Migrate 2 SQL instances to RDS with managed benefits",
            "Monthly Impact": "$300 savings + reduced management",
            "Implementation": "3-4 months migration project",
            "Risk": "Medium - application dependencies"
        }
    ]
    
    specialized_df = pd.DataFrame(specialized_recs)
    st.dataframe(specialized_df, use_container_width=True, hide_index=True)
    
    # Windows specialization deep dive
    st.markdown("### 🔍 Windows Specialization Deep Dive")
    
    tab1, tab2, tab3 = st.tabs(["File Server Migration", "AD Integration", "License Optimization"])
    
    with tab1:
        st.markdown("#### 📁 File Server to FSx Migration Plan")
        
        migration_plan = pd.DataFrame({
            'Phase': ['Phase 1', 'Phase 2', 'Phase 3'],
            'File Servers': ['Critical (5 servers)', 'Department (7 servers)', 'Archive (3 servers)'],
            'FSx Configuration': ['Multi-AZ, 512 MB/s', 'Single-AZ, 64 MB/s', 'Single-AZ, 16 MB/s'],
            'Migration Method': ['AWS DataSync', 'AWS DataSync', 'AWS Storage Gateway'],
            'Timeline': ['Month 1', 'Month 2', 'Month 3'],
            'Risk Level': ['Low', 'Low', 'Very Low']
        })
        
        st.dataframe(migration_plan, use_container_width=True, hide_index=True)
        
        # FSx cost comparison
        fsx_costs = pd.DataFrame({
            'Storage Tier': ['SSD (Frequently accessed)', 'HDD (Infrequently accessed)', 'Backup (S3)'],
            'Current Cost/GB/Month': ['$0.50', '$0.30', '$0.25'],
            'FSx Cost/GB/Month': ['$0.13', '$0.08', '$0.004'],
            'Monthly Savings': ['74%', '73%', '98%']
        })
        
        fig = px.bar(fsx_costs, x='Storage Tier', y=['Current Cost/GB/Month', 'FSx Cost/GB/Month'],
                    title="Storage Cost Comparison: Current vs FSx")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("#### 🔐 Active Directory Integration Architecture")
        
        st.markdown("""
        **Recommended Architecture: AWS Managed Microsoft AD with Trust**
        
        ```
        On-Premises AD Domain          AWS Managed Microsoft AD
        ├── corp.company.com          ├── aws.corp.company.com
        ├── Users: 1,250             ├── AWS-specific accounts
        ├── Computers: 890           ├── EC2 instances
        └── Trust Relationship ←────→ └── FSx file systems
        ```
        """)
        
        ad_benefits = pd.DataFrame({
            'Benefit': ['Seamless FSx Integration', 'Managed Patching', 'High Availability', 'Backup & Recovery', 'Compliance'],
            'Current State': ['Manual setup required', 'Manual patching', 'Single point of failure', 'Manual backup', 'Customer managed'],
            'With AWS Managed AD': ['Automatic integration', 'AWS managed', 'Multi-AZ by default', 'Automated snapshots', 'AWS compliance']
        })
        
        st.dataframe(ad_benefits, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("#### 💰 Windows Licensing ROI Analysis")
        
        # 3-year ROI calculation
        roi_data = pd.DataFrame({
            'Year': ['Year 1', 'Year 2', 'Year 3'],
            'Hybrid Benefit Savings': [44160, 44160, 44160],  # $3,680 * 12
            'Storage Savings': [21600, 21600, 21600],  # $1,800 * 12
            'Operational Savings': [6000, 8000, 10000],  # Increasing efficiency
            'Total Annual Savings': [71760, 73760, 75760],
            'Cumulative Savings': [71760, 145520, 221280]
        })
        
        fig = px.line(roi_data, x='Year', y='Cumulative Savings',
                     title="3-Year Cumulative Savings from Windows Specialization",
                     markers=True)
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("💰 **3-Year Total Savings: $221,280** with Windows & Storage specialization")
    
    # Amazon Q specialized assistance
    st.markdown("### 🤖 Amazon Q - Windows & Storage Specialist")
    user_question = st.text_input("Ask about Windows & Storage optimization...", 
                                placeholder="e.g., How do I migrate file servers with minimal downtime?")
    
    if user_question:
        one_ola_responses = {
            "migrate": "For minimal downtime file server migration: 1) Use AWS DataSync for initial sync while servers are live, 2) Schedule final sync during maintenance window, 3) Update DNS/DFS to point to FSx, 4) Test access before decommissioning old servers. Typical downtime: 2-4 hours per server.",
            "fsx": "FSx for Windows File Server provides native SMB/CIFS protocol, integrates with Active Directory, supports DFS, and includes automated backups. It's specifically designed to replace Windows file servers with better performance and lower cost.",
            "licensing": "Windows Hybrid Benefit can save 40-50% on Windows Server costs. You can apply existing on-premises licenses to AWS EC2 instances. For SQL Server, compare BYOL on EC2 vs RDS License Included based on your usage patterns.",
            "ad": "AWS Managed Microsoft AD is recommended for Windows-heavy environments. It provides full AD features, integrates seamlessly with FSx, and can establish trust relationships with on-premises AD for hybrid scenarios.",
            "default": "Your Windows-heavy environment (85% Windows) is perfect for ONE OLA specialization. Focus on: 1) Immediate Hybrid Benefit application ($3,680/month savings), 2) File server consolidation to FSx ($1,800/month savings), 3) AD integration for seamless management. Total potential: 52% cost reduction."
        }
        
        response_key = "default"
        if "migrate" in user_question.lower() or "downtime" in user_question.lower():
            response_key = "migrate"
        elif "fsx" in user_question.lower() or "file" in user_question.lower():
            response_key = "fsx"
        elif "licens" in user_question.lower() or "hybrid" in user_question.lower():
            response_key = "licensing"
        elif "active directory" in user_question.lower() or "ad" in user_question.lower():
            response_key = "ad"
        
        st.markdown(f"**Amazon Q (Windows & Storage Specialist):** {one_ola_responses[response_key]}")
    
    # Export specialized results
    st.markdown("### 📄 Export Windows & Storage Specialization Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🖥️ Windows Optimization Report"):
            st.success("Windows specialization report generated!")
    with col2:
        if st.button("💾 Storage Migration Plan"):
            st.success("Detailed storage migration plan exported!")
    with col3:
        if st.button("💰 Licensing Business Case"):
            st.success("Windows licensing ROI analysis exported!")

def create_windows_storage_sample_data():
    """Create sample data for Windows storage analysis"""
    import random
    
    file_servers = []
    server_types = ['Finance-FS', 'HR-FS', 'Engineering-FS', 'Marketing-FS', 'Archive-FS', 'Backup-FS', 'Shared-FS']
    
    for i, server_type in enumerate(server_types):
        capacity = random.choice([500, 1000, 2000, 4000, 8000])
        used_pct = random.randint(60, 90)
        used_gb = int(capacity * used_pct / 100)
        
        file_servers.append({
            'Server_Name': f"{server_type}-{i+1:02d}",
            'Server_Type': server_type.split('-')[0],
            'Capacity_GB': capacity,
            'Used_GB': used_gb,
            'Free_GB': capacity - used_gb,
            'Utilization_%': used_pct,
            'Access_Pattern': random.choice(['High', 'Medium', 'Low']),
            'Backup_Required': random.choice([True, False]),
            'Compliance_Data': random.choice([True, False])
        })
    
    # Add more servers to reach 15
    for i in range(len(file_servers), 15):
        capacity = random.choice([500, 1000, 2000])
        used_pct = random.randint(50, 85)
        used_gb = int(capacity * used_pct / 100)
        
        file_servers.append({
            'Server_Name': f"FileServer-{i+1:02d}",
            'Server_Type': random.choice(['Department', 'Project', 'Archive']),
            'Capacity_GB': capacity,
            'Used_GB': used_gb,
            'Free_GB': capacity - used_gb,
            'Utilization_%': used_pct,
            'Access_Pattern': random.choice(['High', 'Medium', 'Low']),
            'Backup_Required': random.choice([True, False]),
            'Compliance_Data': random.choice([True, False])
        })
    
    return pd.DataFrame(file_servers)

def show_results_dashboard():
    st.subheader("📈 Results Dashboard")
    st.info("Portfolio dashboard showing multiple customer assessments and analytics.")

def create_sample_data():
    """Create sample server data for demonstration"""
    import random
    
    server_names = [f"Server{i:03d}" for i in range(1, 51)]
    os_options = ["Windows Server 2019", "Windows Server 2016", "Linux Ubuntu 20.04", "Linux CentOS 7"]
    
    data = []
    for name in server_names:
        data.append({
            'Server_Name': name,
            'CPU_Cores': random.choice([2, 4, 8, 16]),
            'Memory_GB': random.choice([8, 16, 32, 64]),
            'Storage_GB': random.choice([100, 500, 1000, 2000]),
            'OS': random.choice(os_options),
            'Application_Count': random.randint(1, 5),
            'Storage_Type': random.choice(['SSD', 'HDD', 'SAN'])
        })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    main()

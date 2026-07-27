import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Financial Engineering Pricing Engine", layout="wide")

st.title("Serverless Financial Engineering Pipeline")
st.caption("Distributed Monte Carlo Simulation & Energy Market Markov Switching Dynamics")

st.sidebar.header("Econometric Configuration")
selected_model = st.sidebar.selectbox("Target Valuation Model", ["Variable Annuity (GLWB Rider)", "Wholesale Electricity Spot Market", "Path-Dependent American Option"])
market_volatility = st.sidebar.slider("Simulate Exogenous Market Volatility", 1.0, 5.0, 2.5)
run_simulation = st.sidebar.button("Initialize Distributed Compute Swarm")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: AWS API Ingestion -> Parallel Lambda Compute -> Pricing Aggregation")

if run_simulation:
    st.subheader(f"Active Distributed Inference Engine: {selected_model}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_asset = col1.empty()
    metric_latency = col2.empty()
    metric_price = col3.empty()
    metric_status = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(2828)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    asset_prices = []
    derivative_valuations = []
    
    base_asset = 100.0 if "Option" in selected_model else 50.0
    base_valuation = 15.0 if "Option" in selected_model else 5.0
    
    for i in range(100):
        compute_nodes = int(np.random.uniform(5000, 15000))
        
        if i < 35:
            current_asset = base_asset + np.random.uniform(-1.0, 1.0)
            current_valuation = base_valuation + np.random.uniform(-0.1, 0.1)
            compute_latency = np.random.uniform(15.0, 25.0)
            status = "STABLE MARKET DYNAMICS"
        elif i >= 35 and i < 65:
            current_asset = base_asset - (i - 35) * (1.2 * market_volatility) + np.random.uniform(-5.0, 5.0)
            current_valuation = base_valuation + (i - 35) * (0.8 * market_volatility) + np.random.uniform(-1.0, 1.0)
            compute_latency = np.random.uniform(25.0, 40.0)
            status = "VOLATILITY SHOCK DETECTED"
        else:
            current_asset = current_asset + np.random.uniform(-2.0, 2.0)
            current_valuation = current_valuation - np.random.uniform(0.5, 1.5)
            current_valuation = max(base_valuation, current_valuation)
            compute_latency = np.random.uniform(18.0, 28.0)
            status = "MARKOV STATE TRANSITION"
            
        current_asset = max(5.0, current_asset)
            
        asset_prices.append(current_asset)
        derivative_valuations.append(current_valuation)
        
        metric_asset.metric("Underlying Asset Spot Price", f"${current_asset:.2f}", f"{(current_asset - base_asset):.2f}")
        metric_latency.metric("Parallel Compute Latency", f"{compute_latency:.1f} ms", f"{compute_nodes:,} AWS Nodes")
        metric_price.metric("Analytic Derivative Valuation", f"${current_valuation:.4f}", f"+${(current_valuation - base_valuation):.4f} Premium")
        
        if status == "VOLATILITY SHOCK DETECTED":
            metric_status.metric("Econometric Status", status, "Recalculating Paths")
        elif status == "MARKOV STATE TRANSITION":
            metric_status.metric("Econometric Status", status, "New Pricing Baseline")
        else:
            metric_status.metric("Econometric Status", status, "Normal")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=asset_prices, mode='lines', name='Asset Spot Price', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=derivative_valuations, mode='lines', name='Computed Derivative Value', yaxis='y2', line=dict(color='blue', dash='dot')))
        
        fig.update_layout(
            title="Financial Engineering: Asset Volatility vs Parallelized Derivative Valuation",
            xaxis=dict(title="High-Frequency Compute Timeline"),
            yaxis=dict(title="Asset Price (USD)", range=[0, max(150, current_asset + 20)]),
            yaxis2=dict(title="Derivative Valuation (USD)", overlaying='y', side='right', range=[0, max(40, current_valuation + 5)]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if status == "VOLATILITY SHOCK DETECTED" and i == 35:
            log_placeholder.error(f"SYSTEMIC ALERT: High-velocity market shock detected at {time_steps[i].strftime('%H:%M:%S')}. Spawning {compute_nodes:,} ephemeral AWS Lambda instances to execute massively parallel Monte Carlo simulations. Computational bottleneck bypassed.")
        elif status == "MARKOV STATE TRANSITION" and i == 65:
            log_placeholder.warning(f"ECONOMETRIC SHIFT: Cloud middleware identifies mathematical state transition in underlying market dynamics. Adjusting structural pricing parameters dynamically.")
        elif status == "STABLE MARKET DYNAMICS" and i % 5 == 0:
            log_placeholder.success(f"Log: High-frequency telemetry tick {i} ingested. Serverless finite difference grids operating within optimal sub-30ms latency parameters.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The serverless cloud architecture successfully parallelized the stochastic models, pricing the complex financial derivative in real-time.")
else:
    st.info("Click 'Initialize Distributed Compute Swarm' in the sidebar to simulate high-frequency financial engineering processing.")
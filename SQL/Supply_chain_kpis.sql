SELECT 
    ProductType,
    CarrierName,
    COUNT(ShipmentID) AS total_shipments,

    ROUND(SUM(ProductValue_INR), 2) AS total_product_value_inr,
    ROUND(SUM(ShippingCost_INR), 2) AS total_shipping_cost_inr,
    
    
    ROUND((SUM(OnTimeDeliveryFlag) / COUNT(ShipmentID)) * 100, 2) AS on_time_delivery_rate_pct,
    
    
    COUNT(CASE WHEN ShipmentStatus = 'Cancelled' THEN 1 END) AS cancelled_shipments,
    COUNT(CASE WHEN ShipmentStatus = 'Delayed' THEN 1 END) AS delayed_shipments,
    

    ROUND(AVG(Weight_KG), 2) AS avg_weight_kg,
    ROUND(AVG(Distance_KM), 2) AS avg_distance_km

FROM 
    `lofty-proton-512605-u0.supply_chain_data.cleaned_shipments_data`
GROUP BY 
    ProductType, CarrierName
ORDER BY 
    total_shipments DESC;

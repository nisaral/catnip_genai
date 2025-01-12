import React, { useState } from 'react';
import axios from 'axios';

const ShipmentOrderDetails = () => {
  const [orderData, setOrderData] = useState({
    orderId: '',
    customerName: '',
    productDescription: '',
    orderStatus: '',
  });

  const [shipmentData, setShipmentData] = useState({
    trackingId: '',
    shippingAddress: '',
    shipmentStatus: '',
    productDescription: '',
  });

  const [productData, setProductData] = useState({
    productId: '',
    productName: '',
    productDescription: '',
    price: '',
    productCategory: '',
  });

  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', {
        orderData,
        shipmentData,
        productData,
      });
      setPredictions(response.data);
    } catch (error) {
      console.error("Error fetching predictions:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h3 className="font-bold text-lg mb-4">Shipment and Order Predictions</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <h4 className="font-medium">Order Details</h4>
          <input
            type="text"
            placeholder="Order ID"
            value={orderData.orderId}
            onChange={(e) => setOrderData({ ...orderData, orderId: e.target.value })}
            className="w-full p-2 border rounded mt-2"
          />
          <input
            type="text"
            placeholder="Customer Name"
            value={orderData.customerName}
            onChange={(e) => setOrderData({ ...orderData, customerName: e.target.value })}
            className="w-full p-2 border rounded mt-2"
          />
          <input
            type="text"
            placeholder="Product Description"
            value={orderData.productDescription}
            onChange={(e) => setOrderData({ ...orderData, productDescription: e.target.value })}
            className="w-full p-2 border rounded mt-2"
          />
          <input
            type="text"
            placeholder="Order Status"
            value={orderData.orderStatus}
            onChange={(e) => setOrderData({ ...orderData, orderStatus: e.target.value })}
            className="w-full p-2 border rounded mt-2"
          />
        </div>
        <div>
          <h4 className="font-medium">Shipment Details</h4>
          <input
            type="text"
            placeholder="Tracking ID"
            value={shipmentData.trackingId}
            onChange={(e) => setShipmentData({ ...shipmentData, trackingId: e.target.value })}
            className="w-full p-2 border rounded mt-2"
          />
          <input
            type="text"
            placeholder="Shipping Address"
            value={shipmentData.shippingAddress}
            onChange={(e) => setShipmentData({ ...shipmentData, shippingAddress: e.target.value })}
            className="w-full p-2 border rounded mt-2"
          />
          <input
            type="text"
            placeholder="Shipment Status"
            value={shipmentData.shipmentStatus}
            onChange={(e) => setShipmentData({ ...shipmentData, shipmentStatus: e.target.value })}
            className="w-full p-2 border rounded mt-2"
          />
        </div>
        <div>
          <h4 className="font-medium">Product Details</h4>
          <input
            type="text"
            placeholder="Product ID"
            value={productData.productId}
            onChange={(e) => setProductData({ ...productData, productId: e.target.value })}
            className="w-full p-2 border rounded mt-2"
          />
          <input
            type="text"
            placeholder="Product Name"
            value={productData.productName}
            onChange={(e) => setProductData({ ...productData, productName: e.target.value })}
            className="w-full p-2 border rounded mt-2"
          />
        </div>
      </div>
      <button
        onClick={handlePredict}
        disabled={loading}
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-blue-300"
      >
        {loading ? 'Loading...' : 'Get Predictions'}
      </button>
      {predictions && (
        <div className="mt-4">
          <h4 className="font-medium">Predictions</h4>
          <pre className="p-4 bg-gray-100 rounded">{JSON.stringify(predictions, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default ShipmentOrderDetails;

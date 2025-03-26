import React, { useState } from "react";
import './index.css';
import axios from "axios";

function App() {
  const [features, setFeatures] = useState(Array(6).fill(""));
  const [prediction, setPrediction] = useState("");

  const handleInputChange = (index, value) => {
    const newFeatures = [...features];
    newFeatures[index] = value;
    setFeatures(newFeatures);
  };

  const predictMaterial = async () => {
    try {
        const featureKeys = ["Su", "Sy", "E", "G", "mu", "Ro"];
        const featureObject = featureKeys.reduce((obj, key, index) => {
            obj[key] = Number(features[index]);
            return obj;
        }, {});

        const response = await axios.post("http://127.0.0.1:5000/predict", featureObject, {
            headers: {
                "Content-Type": "application/json"
            }
        });
        console.log("Prediction:", response.data.predicted_material);
        setPrediction(response.data.predicted_material);
    } catch (error) {
        console.error("Prediction error:", error);
        setPrediction("Error occurred during prediction");
    }
};


  return (
    <div className="wind">
  <h2 className="heading">Material Classification</h2>
  <table style={{ margin: "0 auto", borderCollapse: "collapse" }}>
    <tbody>
      {[
        "Ultimate Tensile Strength (Su) in MPa",
        "Yield Strength (Sy) in MPa",
        "Elastic Modulus (E) in MPa",
        "Shear Modulus (G) in MPa",
        "Poisson's Ratio (mu)",
        "Density (Ro) in Kg/m3",
      ].map((feature, index) => (
        <tr key={index}>
          <td style={{ padding: "8px", border: "1px solid transparent", textAlign: "right" }}>
            <label>{feature}:</label>
          </td>
          <td style={{ padding: "8px", border: "1px solid transparent" }}>
            <input
              type="number"
              onChange={(e) => handleInputChange(index, e.target.value)}
              style={{ padding: "5px", width: "100%", borderRadius: "4px", border: "1px solid #ddd" }}
            />
          </td>
        </tr>
      ))}
    </tbody>
  </table>
  <button
    onClick={predictMaterial}
    className="sub-but"
  >
    Predict Material
  </button>
  {prediction && (
    <h3 style={{ marginTop: "20px" }}>Predicted Material: {prediction}</h3>
  )}
</div>

  );
}

export default App;
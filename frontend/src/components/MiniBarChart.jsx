import React from 'react';
import { C } from "../constants/theme";

const MiniBarChart = ({ data = [10, 40, 30, 50, 20] }) => {
    const max = Math.max(...data);

    return (
        <div style={{ display: "flex", alignItems: "flex-end", gap: 4, height: 64, padding: "0 8px" }}>
            {data.map((val, i) => (
                <div
                    key={i}
                    style={{
                        height: `${(val / max) * 100}%`,
                        background: C.accent,
                        width: 12,
                        borderRadius: "2px 2px 0 0",
                        boxShadow: `0 0 5px ${C.accent}44`
                    }}
                    title={`Value: ${val}`}
                ></div>
            ))}
        </div>
    );
};

export default MiniBarChart;

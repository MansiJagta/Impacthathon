import { C } from "../constants/theme";

export function GaugeBar({ label, val }) {
    return (
        <div style={{ marginBottom: 12 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                <span style={{ color: C.muted, fontSize: 11 }}>{label}</span>
                <span style={{ color: C.text, fontSize: 11, fontWeight: 700 }}>{val}</span>
            </div>
            <div style={{ background: "rgba(255,255,255,0.05)", borderRadius: 4, height: 6 }}>
                <div style={{
                    width: `${val * 100}%`, height: 6, borderRadius: 4,
                    background: val > 0.5 ? C.red : val > 0.3 ? C.yellow : C.green,
                    transition: "width .6s",
                    boxShadow: `0 0 10px ${val > 0.5 ? C.red : val > 0.3 ? C.yellow : C.green}44`
                }} />
            </div>
        </div>
    );
}
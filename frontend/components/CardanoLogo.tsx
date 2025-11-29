export default function CardanoLogo({ className = "w-6 h-6" }: { className?: string }) {
  // Official Cardano logo: central dot, 3 concentric rings of dots
  return (
    <svg
      className={className}
      viewBox="0 0 100 100"
      fill="currentColor"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Central dot */}
      <circle cx="50" cy="50" r="6" />
      {/* First ring: 6 dots */}
      {Array.from({ length: 6 }).map((_, i) => {
        const angle = (i * 60) * (Math.PI / 180);
        const x = 50 + 18 * Math.cos(angle);
        const y = 50 + 18 * Math.sin(angle);
        return <circle key={i} cx={x} cy={y} r="3.5" />;
      })}
      {/* Second ring: 12 dots */}
      {Array.from({ length: 12 }).map((_, i) => {
        const angle = (i * 30) * (Math.PI / 180);
        const x = 50 + 30 * Math.cos(angle);
        const y = 50 + 30 * Math.sin(angle);
        return <circle key={i+6} cx={x} cy={y} r="2.5" />;
      })}
      {/* Third ring: 18 dots */}
      {Array.from({ length: 18 }).map((_, i) => {
        const angle = (i * 20) * (Math.PI / 180);
        const x = 50 + 40 * Math.cos(angle);
        const y = 50 + 40 * Math.sin(angle);
        return <circle key={i+18} cx={x} cy={y} r="1.8" />;
      })}
    </svg>
  );
}

export default function AISymbol({ className = "w-6 h-6" }: { className?: string }) {
  // Abstract AI symbol: neural network node/circuit style, modern and clean
  return (
    <span className={className} style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="16" cy="16" r="12" stroke="#7C3AED" strokeWidth="2" fill="#fff" />
        <circle cx="16" cy="16" r="4" fill="#7C3AED" />
        <circle cx="8" cy="16" r="2" fill="#7C3AED" />
        <circle cx="24" cy="16" r="2" fill="#7C3AED" />
        <circle cx="16" cy="8" r="2" fill="#7C3AED" />
        <circle cx="16" cy="24" r="2" fill="#7C3AED" />
        <line x1="16" y1="8" x2="16" y2="12" stroke="#7C3AED" strokeWidth="1.5" />
        <line x1="16" y1="20" x2="16" y2="24" stroke="#7C3AED" strokeWidth="1.5" />
        <line x1="8" y1="16" x2="12" y2="16" stroke="#7C3AED" strokeWidth="1.5" />
        <line x1="20" y1="16" x2="24" y2="16" stroke="#7C3AED" strokeWidth="1.5" />
      </svg>
    </span>
  );
}

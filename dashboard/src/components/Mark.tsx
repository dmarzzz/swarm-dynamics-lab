/** Brand mark: seven headings aligning, a tiny Vicsek flock. */
export function Mark({ className }: { className?: string }) {
  const birds = [
    [4, 13, -32], [8, 9, -36], [12, 12, -40], [9, 15, -38], [14, 7, -42], [16, 11, -44], [6, 6, -30],
  ];
  return (
    <svg className={className} viewBox="0 0 20 20" aria-hidden="true">
      {birds.map(([x, y, a], i) => (
        <g key={i} transform={`translate(${x} ${y}) rotate(${a})`}>
          <path d="M-2 -1.1 L2.2 0 L-2 1.1 Z" fill={i === 4 ? 'var(--accent)' : 'currentColor'} />
        </g>
      ))}
    </svg>
  );
}

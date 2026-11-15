// DDC-CWICR-OE: DataDrivenConstruction · OpenBusinessERP
// Copyright (c) 2026 Artem Boiko / DataDrivenConstruction
import clsx from 'clsx';

interface LogoProps {
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  animate?: boolean;
  className?: string;
}

/* Icon sizes — compact so the text dominates */
const sizeMap = {
  xs: 'h-5 w-5',
  sm: 'h-6 w-6',
  md: 'h-7 w-7',
  lg: 'h-10 w-10',
  xl: 'h-14 w-14',
};

/**
 * Brand mark: a flat blue tile with a "B" built from a spine and two ledger
 * blocks. Flat colour on purpose, so it prints and favicons cleanly.
 * `animate` is accepted for API compatibility and has no effect.
 */
export function Logo({ size = 'md', className }: LogoProps) {
  return (
    <div className={clsx(sizeMap[size], 'relative shrink-0', className)}>
      <img src="/logo.svg" alt="" aria-hidden className="h-full w-full rounded-[22%] object-cover" draggable={false} />
    </div>
  );
}

/* ── LogoWithText ──────────────────────────────────────────────────────── */

interface LogoWithTextProps extends LogoProps {
  showVersion?: boolean;
}

/* Text sizes — larger than icon to make the name prominent */
const textSizeMap = {
  xs: 'text-[15px] leading-none',
  sm: 'text-[16px] leading-none',
  md: 'text-[17px] leading-none',
  lg: 'text-xl leading-none',
  xl: 'text-2xl leading-none',
};

const gapSizeMap = {
  xs: 'gap-1.5',
  sm: 'gap-2',
  md: 'gap-2',
  lg: 'gap-2.5',
  xl: 'gap-3',
};

/**
 * Logo + brand name. Per BRAND.md:
 * - Font: Plus Jakarta Sans 800
 * - Name: "Archi Savvy Studio ERP" (PascalCase, one word)
 * - Letter-spacing: -0.02em
 * - Icon is compact, name is prominent
 */
export function LogoWithText({ size = 'md', animate, showVersion = true, className }: LogoWithTextProps) {
  return (
    <div className={clsx('flex items-center', gapSizeMap[size], className)}>
      <Logo size={size} animate={animate} />
      <span
        className={clsx(
          textSizeMap[size],
          'font-medium text-content-primary whitespace-nowrap tracking-tight',
        )}
        style={{ fontFamily: "'Plus Jakarta Sans', system-ui, sans-serif", letterSpacing: '-0.02em' }}
      >
        Archi <span className="font-semibold">Savvy</span>
        {showVersion && <span className="text-content-tertiary"> Studio ERP</span>}
      </span>
    </div>
  );
}

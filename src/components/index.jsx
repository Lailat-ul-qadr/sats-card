import React from 'react';

/* ---------------------------------------------------------------- */
/* Logo / Brand mark                                                 */
/* ---------------------------------------------------------------- */
export const Logo = ({ size = 'md', className = '' }) => {
  const sizes = {
    sm: 'w-6 h-6 text-sm',
    md: 'w-9 h-9 text-lg',
    lg: 'w-12 h-12 text-2xl',
  };
  return (
    <div className={`flex items-center gap-2.5 ${className}`}>
      <div className={`${sizes[size]} rounded-xl bg-amber-lime flex items-center justify-center font-display font-bold text-bg shrink-0`}>
        ⚡
      </div>
      <span className="font-display font-bold text-ink tracking-tight text-lg">Mobibit Africa</span>
    </div>
  );
};

/* ---------------------------------------------------------------- */
/* Button                                                             */
/* ---------------------------------------------------------------- */
export const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  className = '',
  ...props
}) => {
  const baseStyles = 'font-sans font-semibold rounded-xl transition-all duration-200 inline-flex items-center justify-center gap-2 whitespace-nowrap select-none';

  const variants = {
    primary: 'bg-amber-lime text-bg shadow-glow-amber-sm hover:brightness-110 hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:pointer-events-none',
    secondary: 'bg-elevated border border-line text-ink hover:border-amber/60 hover:text-amber disabled:opacity-50',
    outline: 'border border-line text-ink-soft hover:border-amber hover:text-amber bg-transparent disabled:opacity-50',
    ghost: 'text-ink-soft hover:text-ink hover:bg-white/5 disabled:opacity-50',
    danger: 'bg-danger/15 border border-danger/40 text-danger hover:bg-danger/25 disabled:opacity-50',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-5 py-2.5 text-sm',
    lg: 'px-7 py-3.5 text-base',
  };

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};

/* ---------------------------------------------------------------- */
/* Input                                                              */
/* ---------------------------------------------------------------- */
export const Input = ({
  label,
  error,
  helperText,
  className = '',
  type: inputType,
  ...props
}) => {
  const [showPassword, setShowPassword] = React.useState(false);
  const isPassword = inputType === 'password';
  const resolvedType = isPassword && showPassword ? 'text' : inputType;

  return (
    <div className="flex flex-col">
      {label && (
        <label className="text-xs font-semibold text-ink-muted mb-2 uppercase tracking-wider">
          {label}
        </label>
      )}
      <div className="relative">
        <input
          type={resolvedType}
          className={`px-4 py-3 bg-surface border rounded-xl font-sans text-base text-ink placeholder:text-ink-muted transition-colors ${isPassword ? 'pr-12' : ''} ${error ? 'border-danger' : 'border-line'} ${className}`}
          {...props}
        />
        {isPassword && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-ink-muted hover:text-ink transition-colors p-1"
            tabIndex={-1}
          >
            {showPassword ? (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            ) : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
            )}
          </button>
        )}
      </div>
      {helperText && (
        <p className={`text-xs mt-1.5 ${error ? 'text-danger' : 'text-ink-muted'}`}>
          {helperText}
        </p>
      )}
    </div>
  );
};

/* ---------------------------------------------------------------- */
/* Card (generic panel)                                               */
/* ---------------------------------------------------------------- */
export const Card = ({ children, className = '', ...props }) => {
  return (
    <div
      className={`panel p-6 ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

/* ---------------------------------------------------------------- */
/* Badge                                                              */
/* ---------------------------------------------------------------- */
export const Badge = ({ children, variant = 'default', className = '' }) => {
  const variants = {
    default: 'bg-white/5 text-ink-soft border border-line',
    success: 'bg-success/10 text-success border border-success/30',
    error: 'bg-danger/10 text-danger border border-danger/30',
    warning: 'bg-warning/10 text-warning border border-warning/30',
    info: 'bg-info/10 text-info border border-info/30',
    amber: 'bg-amber/10 text-amber border border-amber/30',
    lime: 'bg-lime/10 text-lime border border-lime/30',
  };

  return (
    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ${variants[variant]} ${className}`}>
      {children}
    </span>
  );
};

/* ---------------------------------------------------------------- */
/* Modal                                                              */
/* ---------------------------------------------------------------- */
export const Modal = ({ isOpen, onClose, title, children, className = '' }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className={`panel-elevated max-w-md w-full ${className}`}>
        <div className="flex justify-between items-center p-6 border-b border-line">
          <h2 className="heading-4">{title}</h2>
          <button onClick={onClose} className="text-ink-muted hover:text-ink transition-colors">
            ✕
          </button>
        </div>
        <div className="p-6">
          {children}
        </div>
      </div>
    </div>
  );
};

/* ---------------------------------------------------------------- */
/* Alert                                                              */
/* ---------------------------------------------------------------- */
export const Alert = ({ type = 'info', title, message, onClose, className = '' }) => {
  const alertStyles = {
    success: 'bg-success/10 border-l-4 border-success text-success',
    error: 'bg-danger/10 border-l-4 border-danger text-danger',
    warning: 'bg-warning/10 border-l-4 border-warning text-warning',
    info: 'bg-info/10 border-l-4 border-info text-info',
  };

  // Support multiline messages by splitting on \n
  const lines = (message || '').split('\n').filter(Boolean);

  return (
    <div className={`${alertStyles[type]} p-4 rounded-lg ${className}`}>
      {title && <h4 className="font-semibold mb-1">{title}</h4>}
      {lines.length > 1 ? (
        <div className="text-sm text-ink-soft space-y-1">
          {lines.map((line, i) => <p key={i}>{line}</p>)}
        </div>
      ) : (
        <p className="text-sm text-ink-soft">{message}</p>
      )}
      {onClose && (
        <button onClick={onClose} className="ml-4 font-semibold">✕</button>
      )}
    </div>
  );
};

/* ---------------------------------------------------------------- */
/* Loading                                                            */
/* ---------------------------------------------------------------- */
export const Loading = () => (
  <div className="min-h-screen flex flex-col items-center justify-center bg-bg py-12">
    <div className="w-10 h-10 border-4 border-line border-t-amber rounded-full animate-spin"></div>
    <p className="text-ink-muted mt-4 text-sm">Loading...</p>
  </div>
);

/* ---------------------------------------------------------------- */
/* EmptyState                                                         */
/* ---------------------------------------------------------------- */
export const EmptyState = ({ icon = '📦', title, description }) => (
  <div className="flex flex-col items-center justify-center py-16 text-center">
    <span className="text-4xl mb-4 opacity-70">{icon}</span>
    <h3 className="heading-4 text-ink">{title}</h3>
    <p className="text-ink-muted mt-2 max-w-md text-sm">{description}</p>
  </div>
);

/* ---------------------------------------------------------------- */
/* Skeleton                                                           */
/* ---------------------------------------------------------------- */
export const Skeleton = ({ count = 1, height = 'h-4', className = '' }) => {
  return (
    <div className="space-y-2">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className={`bg-elevated rounded animate-pulse ${height} ${className}`}
        ></div>
      ))}
    </div>
  );
};

/* ---------------------------------------------------------------- */
/* StatCard - dashboard summary tile                                  */
/* ---------------------------------------------------------------- */
export const StatCard = ({ label, value, sub, accent = 'amber', icon, className = '' }) => {
  const accents = {
    amber: 'from-amber/15 to-transparent border-amber/20',
    lime: 'from-lime/15 to-transparent border-lime/20',
    success: 'from-success/15 to-transparent border-success/20',
    neutral: 'from-white/5 to-transparent border-line',
  };
  return (
    <div className={`relative overflow-hidden panel bg-gradient-to-br ${accents[accent]} p-6 hover:-translate-y-0.5 transition-transform`}>
      <div className="flex items-start justify-between mb-4">
        <p className="text-ink-muted text-xs font-semibold uppercase tracking-wider">{label}</p>
        {icon && <span className="text-xl opacity-80">{icon}</span>}
      </div>
      <p className="font-figures text-2xl md:text-3xl font-bold text-ink">{value}</p>
      {sub && <p className="text-ink-muted text-xs mt-2">{sub}</p>}
    </div>
  );
};

/* ---------------------------------------------------------------- */
/* PageHeader - consistent sub-page header w/ back button             */
/* ---------------------------------------------------------------- */
export const PageHeader = ({ title, onBack, actions }) => (
  <div className="border-b border-line bg-surface/60 backdrop-blur sticky top-0 z-20">
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-5 flex items-center gap-4">
      {onBack && (
        <button
          onClick={onBack}
          className="w-9 h-9 rounded-lg border border-line flex items-center justify-center text-ink-soft hover:text-amber hover:border-amber/50 transition-colors shrink-0"
          aria-label="Go back"
        >
          ←
        </button>
      )}
      <h1 className="heading-3 text-ink flex-1">{title}</h1>
      {actions}
    </div>
  </div>
);

/* ---------------------------------------------------------------- */
/* Toast - lightweight feedback snackbar                              */
/* ---------------------------------------------------------------- */
let _toastTimer = null;

export const Toast = ({ message, type = 'success', visible, onDismiss }) => {
  React.useEffect(() => {
    if (visible) {
      clearTimeout(_toastTimer);
      _toastTimer = setTimeout(() => onDismiss?.(), 2500);
    }
    return () => clearTimeout(_toastTimer);
  }, [visible, onDismiss]);

  const toastVariants = {
    success: 'bg-success/20 border-success/40 text-success',
    error: 'bg-danger/20 border-danger/40 text-danger',
    info: 'bg-info/20 border-info/40 text-info',
  };
  const toastIconMap = { success: '✓', error: '✕', info: 'ℹ' };

  if (!visible) return null;

  return (
    <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 animate-fadeInUp">
      <div className={`flex items-center gap-3 px-5 py-3 rounded-xl border backdrop-blur-sm shadow-lg ${toastVariants[type]}`}>
        <span className="font-bold text-sm">{toastIconMap[type]}</span>
        <span className="text-sm font-medium text-ink">{message}</span>
      </div>
    </div>
  );
};

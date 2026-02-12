import React from 'react';
import { cn } from '../../lib/utils';

const Card = React.forwardRef(({ className, children, title, description, footer, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn(
        'rounded-xl border bg-card text-card-foreground shadow-sm transition-all duration-200 hover:shadow-md dark:border-gray-800 dark:bg-gray-900',
        className
      )}
      {...props}
    >
      {(title || description) && (
        <div className="flex flex-col space-y-1.5 p-6">
          {title && <h3 className="font-semibold leading-none tracking-tight">{title}</h3>}
          {description && <p className="text-sm text-muted-foreground">{description}</p>}
        </div>
      )}
      <div className="p-6 pt-0">{children}</div>
      {footer && <div className="flex items-center p-6 pt-0">{footer}</div>}
    </div>
  );
});

Card.displayName = "Card";

export { Card };

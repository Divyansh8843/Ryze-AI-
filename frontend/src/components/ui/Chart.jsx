import React from 'react';
import { cn } from '../../lib/utils';

const Chart = ({ type = 'bar', data, title, className, ...props }) => {
  // Mock data if not provided or invalid structure
  const chartData = data?.datasets?.[0]?.data || [10, 25, 60, 40, 100, 30];
  const labels = data?.labels || ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
  const maxVal = Math.max(...chartData);

  return (
    <div className={cn("rounded-lg border bg-card p-6 shadow-sm dark:bg-gray-900 dark:border-gray-800", className)} {...props}>
      {title && <h3 className="mb-4 text-sm font-medium text-muted-foreground">{title}</h3>}
      <div className="flex h-[200px] items-end justify-between gap-2 pt-4">
        {chartData.map((value, i) => (
          <div key={i} className="group relative flex h-full w-full flex-col justify-end items-center">
             <div className="relative w-full bg-gray-100 rounded-t-sm dark:bg-gray-800 overflow-hidden h-full">
                <div 
                    className="absolute bottom-0 left-0 right-0 bg-blue-500 transition-all duration-500 ease-out group-hover:bg-blue-600 dark:bg-blue-600 dark:group-hover:bg-blue-500"
                    style={{ height: `${(value / maxVal) * 100}%` }}
                />
             </div>
            <span className="mt-2 text-[10px] text-muted-foreground">{labels[i]}</span>
             {/* Tooltip */}
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 rounded bg-black px-2 py-1 text-xs text-white opacity-0 transition-opacity group-hover:opacity-100 dark:bg-white dark:text-black">
              {value}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export { Chart };

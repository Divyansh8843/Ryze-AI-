import React from 'react';
import { cn } from '../../lib/utils';
import * as LucideIcons from 'lucide-react';

const Sidebar = ({ items, activeItem, position = 'left', className, ...props }) => {
  return (
    <aside
      className={cn(
        "flex h-screen w-64 flex-col overflow-y-auto bg-gray-50 border-r border-gray-200 dark:border-gray-800 dark:bg-gray-900 transition-width duration-300",
        position === 'right' && "border-l border-r-0 order-last",
        className
      )}
    >
      <div className="flex items-center justify-center p-6 border-b border-gray-200 dark:border-gray-800">
        <h1 className="text-xl font-bold tracking-tighter text-gray-900 dark:text-white">
          Menu
        </h1>
      </div>
      <nav className="flex-1 space-y-1 px-3 py-4">
        {items.map((item) => {
          const Icon = LucideIcons[item.icon] || LucideIcons.Circle; // Dynamic icon lookup
          const isActive = activeItem === item.label;

          return (
            <button
              key={item.label}
              onClick={item.onClick}
              className={cn(
                "group flex w-full items-center rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white",
                isActive ? "bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400" : "text-gray-700 dark:text-gray-400"
              )}
            >
              <Icon
                className={cn(
                  "mr-3 h-5 w-5 flex-shrink-0 transition-colors group-hover:text-gray-900 dark:group-hover:text-white",
                  isActive ? "text-blue-600 dark:text-blue-400" : "text-gray-400 dark:text-gray-500"
                )}
                aria-hidden="true"
              />
              {item.label}
            </button>
          );
        })}
      </nav>
      <div className="p-4 border-t border-gray-200 dark:border-gray-800">
        <p className="text-xs text-center text-gray-400">
          Powered by Ryze AI
        </p>
      </div>
    </aside>
  );
};

export { Sidebar };

import React from 'react';
import { cn } from '../../lib/utils';
import { User, Menu, X, Rocket } from 'lucide-react';

const Navbar = ({ brand = "Ryze AI", links = [], user, className, ...props }) => {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <nav className={cn("bg-white border-b border-gray-200 dark:border-gray-800 dark:bg-gray-900 sticky top-0 z-40 transition-colors", className)} {...props}>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <Rocket className="h-8 w-8 text-blue-600" />
              <span className="ml-2 text-xl font-bold tracking-tight text-gray-900 dark:text-white">
                {brand}
              </span>
            </div>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              {links.map((link) => (
                <a
                  key={link.label}
                  href={link.href}
                  className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-300 dark:hover:text-white dark:hover:border-gray-600"
                >
                  {link.label}
                </a>
              ))}
            </div>
          </div>
          <div className="hidden sm:ml-6 sm:flex sm:items-center">
            {user ? (
              <button className="flex rounded-full bg-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:bg-gray-800 dark:focus:ring-offset-gray-900">
                <span className="sr-only">Open user menu</span>
                <img className="h-8 w-8 rounded-full" src={user.avatar} alt="" />
              </button>
            ) : (
                <div className="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center dark:bg-gray-700">
                  <User className="h-5 w-5 text-gray-500 dark:text-gray-400" />
                </div>
            )}
          </div>
          <div className="-mr-2 flex items-center sm:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 dark:text-gray-400 dark:hover:bg-gray-800"
            >
              <span className="sr-only">Open main menu</span>
              {isOpen ? <X className="block h-6 w-6" /> : <Menu className="block h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {isOpen && (
        <div className="sm:hidden bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800">
          <div className="space-y-1 pt-2 pb-3">
            {links.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-500 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-700 dark:text-gray-300 dark:hover:bg-gray-800"
              >
                {link.label}
              </a>
            ))}
          </div>
          <div className="border-t border-gray-200 dark:border-gray-800 pb-4 pt-4">
            <div className="flex items-center px-4">
              <div className="flex-shrink-0">
                  {user ? (
                    <img className="h-10 w-10 rounded-full" src={user.avatar} alt="" />
                ) : (
                    <div className="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center dark:bg-gray-700">
                        <User className="h-6 w-6 text-gray-500 dark:text-gray-400" />
                    </div>
                )}
              </div>
              <div className="ml-3">
                <div className="text-base font-medium text-gray-800 dark:text-white">{user?.name || "Guest"}</div>
                <div className="text-sm font-medium text-gray-500 dark:text-gray-400">{user?.email || "guest@example.com"}</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export { Navbar };

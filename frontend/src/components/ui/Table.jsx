import React from 'react';
import { cn } from '../../lib/utils';
import { CircleAlert } from 'lucide-react';

const Table = React.forwardRef(({ className, headers, data, caption, ...props }, ref) => {
  return (
    <div className="w-full overflow-hidden rounded-lg border bg-white dark:bg-gray-900 shadow-sm relative">
      <table className={cn("w-full caption-bottom text-sm", className)} ref={ref}>
        {caption && <caption className="p-4 text-xs text-muted-foreground">{caption}</caption>}
        <thead className="bg-gray-50/50 dark:bg-gray-800/50 [&_tr]:border-b">
          <tr className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
            {headers && headers.length > 0 && headers.map((header, index) => (
              <th
                key={index}
                className="h-10 px-4 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0"
              >
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="[&_tr:last-child]:border-0">
          {data && data.length > 0 ? (
            data.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
              >
                {headers && headers.map((header, colIndex) => (
                  <td
                    key={`${rowIndex}-${colIndex}`}
                    className="p-4 align-middle [&:has([role=checkbox])]:pr-0"
                  >
                    {row[header.toLowerCase().replace(/ /g, '_')] ?? row[Object.keys(row)[colIndex]]}
                  </td>
                ))}
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={headers?.length || 1} className="p-4 text-center text-muted-foreground">
                <div className="flex flex-col items-center justify-center py-4">
                  <CircleAlert className="h-8 w-8 text-gray-400 mb-2" />
                  <p>No data available</p>
                </div>
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
});

Table.displayName = "Table";

export { Table };

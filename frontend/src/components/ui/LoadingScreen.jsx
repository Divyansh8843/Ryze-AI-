import React from 'react';
import { motion } from 'framer-motion';

export const LoadingScreen = () => {
  return (
    <div className="flex bg-white/50 backdrop-blur-md dark:bg-black/50 rounded-xl p-8 items-center justify-center gap-4 border border-gray-200 dark:border-gray-800 shadow-xl overflow-hidden relative">
        <div className="absolute inset-x-0 h-[2px] bottom-0 bg-blue-500/20">
          <motion.div 
            className="h-full bg-blue-500"
            initial={{ width: "0%" }}
            animate={{ width: "100%" }}
            transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
          />
        </div>
        
        <div className="relative">
             <div className="absolute -inset-1 rounded-full bg-blue-500 blur-md opacity-20 animate-pulse"></div>
             <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full"
             />
        </div>
        
        <div className="flex flex-col">
            <motion.h3 
                className="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-400"
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 2, repeat: Infinity }}
            >
                Neural Architect
            </motion.h3>
            <p className="text-xs text-gray-500 font-mono">Synthesizing React Components...</p>
        </div>
    </div>
  );
};

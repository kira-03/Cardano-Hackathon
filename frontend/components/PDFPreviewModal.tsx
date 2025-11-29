"use client";

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, FileText, Download, Mail, ExternalLink, Loader2, AlertCircle } from 'lucide-react';

interface PDFPreviewModalProps {
  isOpen: boolean;
  onClose: () => void;
  analysisId: string;
  tokenSymbol: string;
  onOpenEmailModal?: () => void;
}

export default function PDFPreviewModal({
  isOpen,
  onClose,
  analysisId,
  tokenSymbol,
  onOpenEmailModal
}: PDFPreviewModalProps) {
  const [isDownloading, setIsDownloading] = useState(false);
  const [error, setError] = useState('');
  
  const pdfUrl = `http://localhost:8000/api/download/pdf/${analysisId}`;

  const handleDownload = async () => {
    setIsDownloading(true);
    setError('');
    
    try {
      const response = await fetch(pdfUrl);
      
      if (!response.ok) {
        throw new Error('Failed to download PDF');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${tokenSymbol}_Analysis_${analysisId.slice(0, 8)}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error: any) {
      setError(error.message || 'Failed to download PDF');
    } finally {
      setIsDownloading(false);
    }
  };

  const handleOpenInNewTab = () => {
    window.open(pdfUrl, '_blank');
  };

  const handleEmailClick = () => {
    if (onOpenEmailModal) {
      onOpenEmailModal();
      onClose();
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-4xl max-h-[90vh] bg-white rounded-2xl shadow-2xl z-50 overflow-hidden flex flex-col"
          >
            {/* Header */}
            <div className="bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-5 text-white flex items-center justify-between flex-shrink-0">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-white/20 rounded-lg">
                  <FileText className="w-6 h-6" />
                </div>
                <div>
                  <h2 className="text-xl font-bold">PDF Report Preview</h2>
                  <p className="text-sm text-white/90 mt-1">
                    {tokenSymbol} Analysis Report
                  </p>
                </div>
              </div>
              
              <button
                onClick={onClose}
                className="text-white/80 hover:text-white transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* PDF Viewer */}
            <div className="flex-1 overflow-hidden bg-gray-100 relative">
              {/* Browser-native PDF viewer */}
              <iframe
                src={pdfUrl}
                className="w-full h-full border-none"
                title={`${tokenSymbol} Analysis Report`}
              />
              
              {/* Fallback message (shows if iframe fails) */}
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div className="bg-white/90 backdrop-blur p-6 rounded-lg shadow-lg max-w-md text-center">
                  <FileText className="w-12 h-12 text-purple-600 mx-auto mb-3" />
                  <p className="text-gray-700 font-medium mb-2">
                    PDF Preview Loading...
                  </p>
                  <p className="text-sm text-gray-600">
                    If the preview doesn't load, use the download or open buttons below.
                  </p>
                </div>
              </div>
            </div>

            {/* Error Message */}
            <AnimatePresence>
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="mx-6 mt-4 flex items-center gap-3 p-3 bg-red-50 border border-red-200 rounded-lg text-red-800"
                >
                  <AlertCircle className="w-5 h-5 flex-shrink-0" />
                  <p className="text-sm font-medium">{error}</p>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Actions */}
            <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex-shrink-0">
              <div className="flex flex-wrap gap-3">
                {/* Download Button */}
                <button
                  onClick={handleDownload}
                  disabled={isDownloading}
                  className="flex-1 min-w-[140px] px-4 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed font-medium flex items-center justify-center gap-2"
                >
                  {isDownloading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Downloading...
                    </>
                  ) : (
                    <>
                      <Download className="w-5 h-5" />
                      Download PDF
                    </>
                  )}
                </button>

                {/* Open in New Tab */}
                <button
                  onClick={handleOpenInNewTab}
                  className="flex-1 min-w-[140px] px-4 py-3 bg-white border-2 border-purple-600 text-purple-600 rounded-lg hover:bg-purple-50 transition-colors font-medium flex items-center justify-center gap-2"
                >
                  <ExternalLink className="w-5 h-5" />
                  Open in Tab
                </button>

                {/* Email Button */}
                {onOpenEmailModal && (
                  <button
                    onClick={handleEmailClick}
                    className="flex-1 min-w-[140px] px-4 py-3 bg-gradient-to-r from-green-600 to-teal-600 text-white rounded-lg hover:shadow-lg transition-all font-medium flex items-center justify-center gap-2"
                  >
                    <Mail className="w-5 h-5" />
                    Email Report
                  </button>
                )}

                {/* Close Button */}
                <button
                  onClick={onClose}
                  className="px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors font-medium"
                >
                  Close
                </button>
              </div>

              {/* Info Text */}
              <p className="text-xs text-gray-500 mt-3 text-center">
                💡 Tip: You can also right-click the preview to save or print the PDF
              </p>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

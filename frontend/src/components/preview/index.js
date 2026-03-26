import TextPreview from './TextPreview';
import ImagePreview from './ImagePreview';
import PDFPreview from './PDFPreview';
import WordPreview from './WordPreview';
import ExcelPreview from './ExcelPreview';
import VideoPreview from './VideoPreview';
import AudioPreview from './AudioPreview';
import FilePreviewContainer from './FilePreviewContainer';
import { fileTypeMapping, getPreviewComponent, getFileExtension, extensionToMimeType } from './fileTypeMapping';

export {
  TextPreview,
  ImagePreview,
  PDFPreview,
  WordPreview,
  ExcelPreview,
  VideoPreview,
  AudioPreview,
  FilePreviewContainer,
  fileTypeMapping,
  getPreviewComponent,
  getFileExtension,
  extensionToMimeType
};
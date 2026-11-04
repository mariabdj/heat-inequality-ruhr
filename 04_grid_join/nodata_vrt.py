r"""Write a small GDAL VRT file that points to a raw raster and declares a no-data value, without changing the raw file."""
import pathlib
from xml.sax.saxutils import escape

import rasterio


def nodata_vrt(src_path, nodata, out_path):
    src_path = pathlib.Path(src_path).resolve()
    with rasterio.open(src_path) as s:
        gt = s.transform.to_gdal()
        dtype = {"uint8": "Byte", "uint16": "UInt16", "int16": "Int16", "float32": "Float32"}[s.dtypes[0]]
        xml = (f'<VRTDataset rasterXSize="{s.width}" rasterYSize="{s.height}">'
               f'<SRS>{escape(s.crs.to_wkt())}</SRS><GeoTransform>{", ".join(repr(v) for v in gt)}</GeoTransform>'
               f'<VRTRasterBand dataType="{dtype}" band="1"><NoDataValue>{nodata}</NoDataValue>'
               f'<SimpleSource><SourceFilename relativeToVRT="0">{escape(str(src_path))}</SourceFilename><SourceBand>1</SourceBand>'
               f'<SrcRect xOff="0" yOff="0" xSize="{s.width}" ySize="{s.height}"/><DstRect xOff="0" yOff="0" xSize="{s.width}" ySize="{s.height}"/>'
               f'</SimpleSource></VRTRasterBand></VRTDataset>')
    pathlib.Path(out_path).write_text(xml, encoding="utf-8")
    return str(out_path)

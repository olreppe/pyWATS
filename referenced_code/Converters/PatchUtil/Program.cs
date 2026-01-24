using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using System.ServiceProcess;


namespace ConverterXMLPatch
{
    class Program
    {
        static int Main(string[] args)
        {
            Console.WriteLine("WATS Patch service (See readme.txt for current actions)");
            string fileName = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData),@"Virinco\WATS\Converters.xml");
            try
            {
                XDocument xDoc = XDocument.Load(fileName);
                XNamespace ns = "http://schemas.virinco.com/WATS/Wats-Client-Service/Converters.xsd";
                IEnumerable<XElement> converters = xDoc.Element(ns + "converters").Elements(ns + "converter").Where(el => el.Attribute("class").Value == "Kone.WATSConverters.LCEConverter");
                foreach (XElement converter in converters)
                {
                    XElement source = converter.Element(ns + "Source");
                    XElement param = source.Elements().Where(el => el.Attribute("name") != null && el.Attribute("name").Value == "PostProcessAction").FirstOrDefault();
                    XElement postProcessAction = new XElement(ns + "Parameter");
                    postProcessAction.Value = "Zip";
                    postProcessAction.SetAttributeValue("name", "PostProcessAction");
                    if (param == null)
                        source.Add(postProcessAction);
                    else
                        param.ReplaceWith(postProcessAction);
                }
                xDoc.Save(fileName);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error patching Converters.xml");
                Console.WriteLine(ex);
                Console.ReadLine();
                return 1;
            }
            try
            {
                ServiceController service = new ServiceController("WATS Client Service");
                if (service.Status == ServiceControllerStatus.Running)
                {
                    Console.WriteLine("Stopping WATS Client Service...");
                    service.Stop();
                    service.WaitForStatus(ServiceControllerStatus.Stopped, new TimeSpan(0, 1, 0));
                    Console.WriteLine("WATS Client Service stopped");
                }
                Console.WriteLine("Starting WATS Client Service...");
                service.Start();
                service.WaitForStatus(ServiceControllerStatus.Running, new TimeSpan(0, 1, 0));
                Console.WriteLine("WATS Client Service started");
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error restarting service");
                Console.WriteLine(ex);
                Console.ReadLine();
                return 2;
            }
            Console.WriteLine("WATS Client patch complete\r\nPress enter to continue");
            Console.ReadLine();            
            return 0;
        }
    }
}


//<?xml version="1.0" encoding="utf-8"?>
//<converters xmlns="http://schemas.virinco.com/WATS/Wats-Client-Service/Converters.xsd">
//  <converter name="TSImporter" assembly="Virinco.WATS.TestStand.Serializer" class="Virinco.WATS.TestStand.Serializer">
//    <Source type="folder">
//      <Parameter name="Path">C:\ProgramData\Virinco\WATS\TSDump</Parameter>
//      <Parameter name="Filter">*.xml</Parameter>
//      <Parameter name="PostProcessAction">Delete</Parameter>
//    </Source>
//    <Destination type="api">
//      <Parameter name="online">False</Parameter>
//    </Destination>
//  </converter>
//  <converter name="WSTFImporter" assembly="Virinco.WATS.Converters.Standard" class="Virinco.WATS.Integration.TextConverter.WATSStandardTextFormat">
//    <Source type="folder">
//      <Parameter name="Path">C:\ProgramData\Virinco\WATS\WatsStandardTextFormat</Parameter>
//      <Parameter name="Filter">*.txt</Parameter>
//      <Parameter name="PostProcessAction">Delete</Parameter>
//    </Source>
//    <Destination type="api">
//      <Parameter name="online">False</Parameter>
//    </Destination>
//  </converter>
//  <converter name="LCEConverter" assembly="Kone.WATSConverters" class="Kone.WATSConverters.LCEConverter">
//    <Source type="folder">
//      <Parameter name="Path">C:\tmp</Parameter>
//      <Parameter name="Filter">*.xml</Parameter>
//      <Parameter name="PostProcessAction">Delete</Parameter>
//    </Source>
//    <Destination type="api">
//      <Parameter name="online">False</Parameter>
//    </Destination>
//  </converter>
//</converters>

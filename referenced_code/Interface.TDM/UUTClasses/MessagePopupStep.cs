extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Represent a popup message box to user.
    /// </summary>
    public class MessagePopupStep : Step
    {
        internal napi.MessagePopupStep _instance;
        internal MessagePopupStep(napi.MessagePopupStep instance) : base(instance) { _instance = instance; }

        /// <summary>
        /// The index of the button pressed in the popup.
        /// </summary>
        public short ButtonPressed
        {
            get => _instance.ButtonPressed;
            set => _instance.ButtonPressed = value;
        }

        /// <summary>
        /// The response text of the popup.
        /// </summary>
        public string Response
        {
            get => _instance.Response;
            set => _instance.Response = value;
        }

        /// <summary>
        /// The number format for the button. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string ButtonFormat
        {
            get => _instance.ButtonFormat;
            set => _instance.ButtonFormat = value;
        }
    }
}

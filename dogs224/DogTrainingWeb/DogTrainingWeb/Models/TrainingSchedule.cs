using System.Text.Json.Serialization;
namespace DogTrainingWeb.Models
{
    public class TrainingSchedule
    {
        public long Id { get; set; }
        // public string? DogName { get; set; }
        public string? StartTime { get; set; }
        // public DateTime EndTime { get; set; }
        [JsonConverter(typeof(JsonStringEnumConverter))]
        public TrainingType TrainingType { get; set; }
    }

    public enum TrainingType
    {
        Base,
        Advanced

    }
}
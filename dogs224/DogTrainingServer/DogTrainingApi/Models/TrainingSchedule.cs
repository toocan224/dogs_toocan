using System.Text.Json.Serialization;

namespace DogTrainingApi.Models // В проекте Web проверь, чтобы namespace был верный (DogTrainingWeb.Models)
{
    public class TrainingSchedule
    {
        public long Id { get; set; }

        // Должно быть строго string! Если тут DateTime — работать не будет.
        public string? StartTime { get; set; } 

        // Чтобы Enum передавался текстом ("Base"), а не числом (0)
        [JsonConverter(typeof(JsonStringEnumConverter))]
        public TrainingType TrainingType { get; set; }
    }

    public enum TrainingType
    {
        Base,
        Advanced,
        Agility
    }
}
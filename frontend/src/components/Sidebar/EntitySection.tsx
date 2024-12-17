import React from "react";
import { Entity } from "../../types/graph";
import EntityList from "../EntityList";

interface EntitySectionProps {
  entities: Entity[];
  onEntityClick: (entity: Entity) => void;
}

const EntitySection: React.FC<EntitySectionProps> = ({
  entities,
  onEntityClick,
}) => {
  const entityTypes = Array.from(new Set(entities.map((e) => e.type)));
  const anomalies = entities.filter((e) => e.isAnomaly);

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-sm font-semibold text-white mb-2">Entity Types</h2>
        <div className="flex flex-wrap gap-2">
          {entityTypes.map((type) => (
            <span
              key={type}
              className="px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-900"
            >
              {type}
            </span>
          ))}
        </div>
      </div>

      {anomalies.length > 0 && (
        <div>
          <h2 className="text-sm font-semibold text-white mb-2">
            Anomalies ({anomalies.length})
          </h2>
          <EntityList entities={anomalies} onEntityClick={onEntityClick} />
        </div>
      )}

      <div>
        <h2 className="text-sm font-semibold text-white mb-2">All Entities</h2>
        <EntityList entities={entities} onEntityClick={onEntityClick} />
      </div>
    </div>
  );
};

export default EntitySection;
